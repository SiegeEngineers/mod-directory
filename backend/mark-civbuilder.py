#! /usr/bin/env python3
import io
import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional, Set

import imagehash
import requests
from PIL import Image

DB_LOCATION = Path(__file__).parent / 'mods.db'


class Database:
    def __init__(self):
        self.db = sqlite3.connect(DB_LOCATION, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def get_rows_to_update(self, count: int):
        result = self.db.execute('''
        SELECT rowid, json
        FROM mods_raw
        WHERE civbuilder IS NULL
        ORDER BY rowid DESC
        LIMIT :count
        ''', {'count': count})
        return result.fetchall()

    def set_civbuilder(self, rowid: int, value: bool):
        parameters = {'value': value, 'rowid': rowid}
        self.cursor.execute('''UPDATE mods_raw SET civbuilder=:value WHERE rowid=:rowid''', parameters)

    def close(self):
        self.db.close()


def get_image_hash(json_str: str) -> Optional[imagehash.ImageHash]:
    data = json.loads(json_str)
    imageUrls = data.get('imageUrls', None)
    if not imageUrls:
        return None
    url = imageUrls[0].get('imageThumbnail', None)
    if not url:
        return None
    else:
        # print(f'Fetching "{url}"')
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            return None
        return imagehash.average_hash(Image.open(io.BytesIO(response.content)))

def load_civbuilder_hashes() -> Set[imagehash.ImageHash]:
    hashes = set()
    folder = Path(__file__).parent / 'civbuilder-images'
    for file in folder.glob('*.jpg'):
        hashes.add(imagehash.average_hash(Image.open(file)))
    return hashes


def main():
    count = 50
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    db = Database()
    hashes = load_civbuilder_hashes()
    try:
        rows_to_update = db.get_rows_to_update(count)
        for row in rows_to_update:
            db.set_civbuilder(row['rowid'], False)
            json_string = row['json']
            if 'krakenmeister.com/civbuilder' in json_string:
                is_civbuilder = True
            else:
                image_hash = get_image_hash(json_string)
                is_civbuilder = image_hash in hashes
            # print(is_civbuilder)
            db.set_civbuilder(row['rowid'], is_civbuilder)
    except Exception as e:
        pass
    db.close()


if __name__ == '__main__':
    main()
