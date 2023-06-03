#! /bin/bash

set -e

cd "$(dirname "$BASH_SOURCE")"

source venv/bin/activate
./scrape.py
./parse-zips.py
