#! /usr/bin/env python3

import json
import sqlite3
import subprocess
import time
import sys
from pathlib import Path
from typing import Dict, List

import requests

CONFIG = json.loads(Path(__file__).with_name('config.json').read_text())
COOKIE_PATH = CONFIG['cookie_path']
COOKIES = json.loads(Path(COOKIE_PATH).read_text())
COOKIE_REFRESH_SCRIPT = CONFIG['cookie_refresh_script']
PAGE_SIZE = 100
RETRIES = 3

FIND_URL = 'https://api.ageofempires.com/api/v4/mods/Find'
DETAILS_URL = 'https://api.ageofempires.com/api/v4/mods/Detail/{mod_id}'
DB_LOCATION = Path(__file__).parent / 'mods.db'


class InvalidCookiesException(Exception):
    pass


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
            json TEXT NOT NULL,
            fileList TEXT DEFAULT NULL,
            civbuilder BOOLEAN DEFAULT NULL
        );''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS mod_tags (
            modRowId int NOT NULL REFERENCES mods_raw(ROWID),
            tag int NOT NULL
        );''')
        self.db.execute('''CREATE INDEX IF NOT EXISTS idx_mod_row_id ON mod_tags (modRowId);''')
        self.db.execute('''CREATE TABLE IF NOT EXISTS mods AS
            SELECT rowid, modId, modName, modTypeId, createDate, lastUpdate, json, fileList, civbuilder
            FROM mods_raw
            WHERE rowid IN (SELECT MAX(rowid) FROM mods_raw GROUP BY modId);
        ''')
        self.db.execute('''CREATE INDEX IF NOT EXISTS idx_create_date ON mods (createDate);''')
        self.db.execute('''CREATE INDEX IF NOT EXISTS idx_last_update ON mods (lastUpdate);''')

    def update_mods_table(self):
        self.db.execute('''DELETE FROM mods WHERE rowid NOT IN (SELECT MAX(rowid) FROM mods_raw GROUP BY modId);''')
        self.db.execute('''INSERT INTO mods (rowid, modId, modName, modTypeId, createDate, lastUpdate, json, fileList, civbuilder)
            SELECT rowid, modId, modName, modTypeId, createDate, lastUpdate, json, fileList, civbuilder
            FROM mods_raw
            WHERE rowid NOT IN (SELECT rowid from mods)
            AND rowid IN (SELECT MAX(rowid) FROM mods_raw GROUP BY modId);
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


def update_cookies():
    global COOKIES
    subprocess.run([COOKIE_REFRESH_SCRIPT], check=True)
    COOKIES = json.loads(Path(COOKIE_PATH).read_text())


def do_full_scan():
    return len(sys.argv) > 1 and sys.argv[1] == 'full'


def main():
    db = Database()
    update_mods(db)
    db.update_mods_table()


def update_mods(db):
    total_count = fetch_total_count()
    print(f'Fetching {total_count} mods')
    pages_count = (total_count - 1) // PAGE_SIZE + 1
    for i in range(1, pages_count + 1):
        print(f'Fetching page {i} of {pages_count}')
        page = fetch_page(i)
        for mod in page:
            mod_id = mod['modId']
            if db.should_update(mod_id, mod['lastUpdate']):
                print(f' Fetching details for mod {mod_id}')
                details = fetch_details(mod_id)
                db.add(details)
            elif not do_full_scan():
                print('Found mod version we already know. Finished!')
                print(f'{mod_id=} at {mod["lastUpdate"]}')
                return


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
                                           'sort': "lastUpdate",
                                           'order': "DESC"},
                                     cookies=COOKIES)
            if response.status_code == 401:
                raise InvalidCookiesException
            rj = response.json()
            return rj['modList']
        except InvalidCookiesException:
            update_cookies()
            time.sleep(5)
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5)
    raise Exception(f'Max retries exceeded for page {i}')


def fetch_total_count() -> int:
    for i in range(1, RETRIES * 10):
        try:
            response = requests.post(FIND_URL, json={'start': 1, 'count': 1, 'q': "", 'game': 2, 'modid': 0,
                                                     'status': "", 'sort': "lastUpdate", 'order': "DESC"},
                                     cookies=COOKIES)
            print(response.text)
            if response.status_code == 401:
                raise InvalidCookiesException
            total_count = response.json()['totalCount']
            if total_count is None:
                print(f'Got None total mods, retrying in  {5 * i} s')
                (Path(__file__).parent / f'response{i}_tmp.json').write_text(response.text)
                time.sleep(5 * i)
                continue
            return total_count
        except InvalidCookiesException:
            update_cookies()
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5 * i)
    raise Exception(f'Max retries exceeded when fetching total count')


def fetch_details(mod_id: int) -> Dict:
    for _ in range(RETRIES):
        try:
            response = requests.get(DETAILS_URL.format(mod_id=mod_id), cookies=COOKIES)
            if response.status_code == 401:
                raise InvalidCookiesException
            return response.json()
        except InvalidCookiesException:
            update_cookies()
        except Exception as e:
            print(f'Oops: {e}')
            time.sleep(5)
    raise Exception(f'Max retries exceeded for mod_id {mod_id}')


if __name__ == '__main__':
    main()
