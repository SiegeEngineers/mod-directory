#! /usr/bin/env python3

import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, List

import requests

COOKIE_PATH = 'cookies.json'
COOKIES = json.loads(Path(COOKIE_PATH).read_text())
PAGE_SIZE = 1000
RETRIES = 3

FIND_URL = 'https://api.ageofempires.com/api/v4/mods/Find'
DETAILS_URL = 'https://api.ageofempires.com/api/v4/mods/Detail/{mod_id}'
DB_LOCATION = Path(__file__).parent / 'mods.db'
TMP_FILE = Path(__file__).parent / 'all_the_mods_tmp.json'
MOD_LIST_FILE = Path(__file__).parent / 'all_the_mods.json'


class Database:
    def __init__(self):
        self.db = sqlite3.connect(DB_LOCATION, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self._init_db()
        self.cursor = self.db.cursor()

    def _init_db(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS mods_raw (
            modId int NOT NULL,
            modName TEXT NOT NULL,
            modTypeId int NOT NULL,
            createDate TEXT NOT NULL,
            lastUpdate TEXT NOT NULL,
            json TEXT NOT NULL
        );''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS mod_tags (
            modRowId int NOT NULL REFERENCES mods_raw(ROWID),
            tag int NOT NULL
        );''')
        self.db.execute('''CREATE VIEW IF NOT EXISTS mods AS 
            SELECT rowid, modId, modName, modTypeId, createDate, lastUpdate, json
            FROM mods_raw
            WHERE rowid IN (SELECT MAX(rowid) FROM mods_raw GROUP BY modId);
        ''')

    def should_update(self, mod_id: int, last_update: str):
        result = self.db.execute('''
        SELECT lastUpdate 
        FROM mods_raw 
        WHERE modId=:modId AND lastUpdate=:lastUpdate
        ''', {'modId': mod_id, 'lastUpdate': last_update})
        return result.fetchone() is None

    def add(self, mod_json: Dict):
        parameters = {key: mod_json[key] for key in ('modId', 'modName', 'modTypeId', 'createDate', 'lastUpdate')}
        parameters['json'] = json.dumps(mod_json, indent=2)
        self.cursor.execute('''INSERT INTO mods_raw (modId, modName, modTypeId, createDate, lastUpdate, json) 
        VALUES (:modId, :modName, :modTypeId, :createDate, :lastUpdate, :json)''', parameters)
        row_id = self.cursor.lastrowid
        params = [{'rowid': row_id, 'tag': tag} for tag in mod_json['modTagIds']]
        self.cursor.executemany('''INSERT INTO mod_tags (modRowId, tag) VALUES (:rowid, :tag)''', params)

    def close(self):
        self.db.close()


def main():
    db = Database()
    mod_list = []
    if TMP_FILE.is_file():
        mod_list = json.loads(TMP_FILE.read_text())
    else:
        total_count = fetch_total_count()
        print(f'Fetching {total_count} mods')
        pages_count = (total_count - 1) // PAGE_SIZE + 1
        for i in range(1, pages_count + 1):
            print(f'Fetching page {i} of {pages_count}')
            page = fetch_page(i)
            mod_list.extend(page)
        TMP_FILE.write_text(json.dumps(mod_list, indent=2))
    for mod in mod_list:
        mod_id = mod['modId']
        # print(f'checking {mod_id=}')
        if db.should_update(mod_id, mod['lastUpdate']):
            print(f'Fetching details for mod {mod_id}')
            details = fetch_details(mod_id)
            db.add(details)
    TMP_FILE.rename(MOD_LIST_FILE)


def fetch_page(i) -> List[Dict]:
    for _ in range(RETRIES):
        try:
            response = requests.post(FIND_URL,
                                     json={'start': i,
                                           'count': PAGE_SIZE,
                                           'q': "",
                                           'game': 2,
                                           'modid': 0,
                                           'status': "",
                                           'sort': "createDate",
                                           'order': "ASC"},
                                     cookies=COOKIES)
            rj = response.json()
            return rj['modList']
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5)
    raise Exception(f'Max retries exceeded for page {i}')

def fetch_total_count() -> int:
    for _ in range(RETRIES):
        try:
            response = requests.post(FIND_URL, json={'start': 1, 'count': 1, 'q': "", 'game': 2, 'modid': 0, 'status': "",
                                                 'sort': "createDate", 'order': "ASC"}, cookies=COOKIES)
            total_count = response.json()['totalCount']
            if total_count is None:
                time.sleep(5)
                continue
            return total_count
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5)
    raise Exception(f'Max retries exceeded when fetching total count')


def fetch_details(mod_id: int) -> Dict:
    for _ in range(RETRIES):
        try:
            response = requests.get(DETAILS_URL.format(mod_id=mod_id), cookies=COOKIES)
            return response.json()
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5)
    raise Exception(f'Max retries exceeded for mod_id {mod_id}')


if __name__ == '__main__':
    main()
