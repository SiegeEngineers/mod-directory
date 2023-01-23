#! /usr/bin/env python3
import io
import json
import sqlite3
import sys
from pathlib import Path
from typing import List
from zipfile import ZipFile, BadZipFile

import requests

DB_LOCATION = Path(__file__).parent / 'mods.db'


class Database:
    def __init__(self):
        self.db = sqlite3.connect(DB_LOCATION, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def get_rows_to_update(self, count: int):
        result = self.db.execute('''
        SELECT rowid, json
        FROM mods
        WHERE fileList IS NULL
        ORDER BY rowid ASC
        LIMIT :count
        ''', {'count': count})
        return result.fetchall()

    def set_file_list(self, rowid: int, file_list: List[str]):
        self._set_file_list(rowid, json.dumps(file_list))

    def set_dummy_file_list(self, rowid: int):
        self._set_file_list(rowid, '["skipped"]')

    def _set_file_list(self, rowid: int, file_list: str):
        parameters = {'file_list': file_list, 'rowid': rowid}
        self.cursor.execute('''UPDATE mods_raw SET fileList=:file_list WHERE rowid=:rowid''', parameters)

    def close(self):
        self.db.close()


def load_file_list(json_str: str) -> List[str]:
    data = json.loads(json_str)
    url = data.get('fileUrl', None)
    size = data.get('modFileSize', 0)
    if size > 500_000_000:
        return [f'skipped due to file size of {size / 1_000_000} MiB']
    if url:
        print(f'Fetching "{url}"')
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return [f'status-code-{response.status_code}']
        try:
            zipfile = ZipFile(io.BytesIO(response.content))
            return zipfile.namelist()
        except BadZipFile:
            return ['bad-zip-file']
        except UnicodeDecodeError:
            return ['unicode-decode-error']
    return ['no-fileUrl-in-json-data']


def main():
    count = 50
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    db = Database()
    rows_to_update = db.get_rows_to_update(count)
    for row in rows_to_update:
        db.set_dummy_file_list(row['rowid'])
        file_list = load_file_list(row['json'])
        db.set_file_list(row['rowid'], file_list)
    db.close()


if __name__ == '__main__':
    main()
