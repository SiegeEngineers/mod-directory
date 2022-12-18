import json
import sqlite3
from enum import Enum
from pathlib import Path
from sqlite3 import Row
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://mods.aoe2.se"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = sqlite3.connect(str(Path(__file__).parent / 'mods.db'), check_same_thread=False)
db.row_factory = sqlite3.Row

PAGE_SIZE = 50


class SortDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class SortColumn(str, Enum):
    createDate = 'createDate'
    lastUpdate = 'lastUpdate'


class QueryData(BaseModel):
    page: int
    sortDirection: SortDirection = SortDirection.DESC
    sortColumn: SortColumn = SortColumn.createDate
    modCategories: List[int]
    searchTerm: str = ''


class ModEntry(BaseModel):
    modId: int
    modName: str
    modTypeId: int
    createDate: str
    lastUpdate: str
    json_str: str
    fileList: Optional[str]


class ModEntryList(BaseModel):
    modEntries: List[ModEntry]
    total: int
    filtered: int
    page: int
    pageSize: int


def to_mod_entry(row: Row) -> ModEntry:
    return ModEntry(
        modId=row['modId'],
        modName=row['modName'],
        modTypeId=row['modTypeId'],
        createDate=row['createDate'],
        lastUpdate=row['lastUpdate'],
        json_str=row['json'],
        fileList=row['fileList'],
    )


@app.post("/api/v1/mods")
def list_mods(query_data: QueryData) -> ModEntryList:
    total = db.execute('select count(distinct(modId)) as c from mods_raw').fetchone()['c']
    mod_type_id_filter = ''
    search_term_filter = ''
    if query_data.modCategories:
        category_placeholders = ','.join([f':modCategory{i}' for i in range(len(query_data.modCategories))])
        mod_type_id_filter = f'WHERE t.tag IN ({category_placeholders})'

    if query_data.searchTerm:
        search_term_filter = f'WHERE m.json LIKE :searchTerm'
        if query_data.modCategories:
            search_term_filter = f'AND m.json LIKE :searchTerm'

    count_query = f'''SELECT COUNT(DISTINCT m.modId) as c
    FROM mods m JOIN mod_tags t ON m.rowid = t.modRowId
    {mod_type_id_filter}
    {search_term_filter}'''

    query = f'''SELECT DISTINCT m.modId, m.modName, m.modTypeId, m.createDate, m.lastUpdate, m.json, m.fileList
    FROM mods m JOIN mod_tags t ON m.rowid = t.modRowId
    {mod_type_id_filter}
    {search_term_filter}
    ORDER BY {query_data.sortColumn} {query_data.sortDirection}
    LIMIT :limit
    OFFSET :offset
    '''

    parameters = {'limit': PAGE_SIZE, 'offset': (query_data.page - 1) * PAGE_SIZE,
                  'searchTerm': f'%{query_data.searchTerm}%'}
    for i, value in enumerate(query_data.modCategories):
        parameters[f'modCategory{i}'] = value
    filtered = db.execute(count_query, parameters).fetchone()['c']
    db_results = db.execute(query, parameters).fetchall()
    results = [to_mod_entry(row) for row in db_results]
    return ModEntryList(modEntries=results, total=total, filtered=filtered, page=query_data.page, pageSize=PAGE_SIZE)


@app.get("/api/v1/mod/{mod_id}")
def single_mod(mod_id: int) -> ModEntryList:
    total = db.execute('select count(distinct(modId)) as c from mods_raw').fetchone()['c']
    query = f'''SELECT modId, modName, modTypeId, createDate, lastUpdate, json, fileList
    FROM mods_raw
    WHERE modId = :modId
    AND rowid in (SELECT MAX(rowid) FROM mods_raw WHERE modId = :modId)
    '''
    db_results = db.execute(query, {'modId': mod_id}).fetchall()
    results = [to_mod_entry(row) for row in db_results]
    return ModEntryList(modEntries=results, total=total, filtered=len(results), page=-1, pageSize=-1)


@app.get("/api/v1/mod/{mod_id}/history")
def mod_history(mod_id: int) -> ModEntryList:
    query = f'''SELECT modId, modName, modTypeId, createDate, lastUpdate, json, fileList
    FROM mods_raw
    WHERE modId = :modId
    ORDER BY rowid DESC
    '''
    db_results = db.execute(query, {'modId': mod_id}).fetchall()
    results = [to_mod_entry(row) for row in db_results]
    return ModEntryList(modEntries=results, total=-1, filtered=len(results), page=-1, pageSize=-1)


@app.get("/api/v1/preview/{mod_id}", response_class=HTMLResponse)
def single_mod(mod_id: int) -> str:
    query = f'''SELECT json
    FROM mods_raw
    WHERE modId = :modId
    AND rowid in (SELECT MAX(rowid) FROM mods_raw WHERE modId = :modId)
    '''
    db_result = db.execute(query, {'modId': mod_id}).fetchone()
    if not db_result:
        raise HTTPException(status_code=404, detail="Mod not found")
    json_content = json.loads(db_result['json'])
    mod_name = json_content['modName']
    description = json_content['description']
    image_url = json_content['imageUrls'][0]['imageThumbnail'] if json_content['imageUrls'] else ''
    author = json_content['creatorName']
    return f'''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{mod_name}</title>
    <!-- Facebook Open Graph -->
    <meta property="og:site_name" content="mods.aoe2.se"/>
    <meta property="og:title" content="{mod_name}"/>
    <meta property="og:url" content="https://mods.aoe2.se/{mod_id}"/>
    <meta property="og:type" content="article"/>
    <meta property="og:description" content="{description}"/>
    <meta property="og:image" content="{image_url}"/>
    <meta property="og:image:width" content="400"/>
    <meta property="og:image:height" content="225"/>
    <!-- Schema.org -->
    <meta itemprop="name" content="AoE2 DE Mod"/>
    <meta itemprop="headline" content="{mod_name}"/>
    <meta itemprop="description" content="{description}"/>
    <meta itemprop="image" content="{image_url}"/>
    <meta itemprop="author" content="{author}"/>
    <!-- Twitter Cards -->
    <meta name="twitter:title" content="{mod_name}"/>
    <meta name="twitter:url" content="https://mods.aoe2.se/{mod_id}"/>
    <meta name="twitter:description" content="{description}"/>
    <meta name="twitter:image" content="{image_url}"/>
    <meta name="twitter:card" content="summary"/>
</head>
<body>
This is a preview generated for preview bots.
</body>
'''
