# mod-directory

An overview over mods on the mod center


## develop

### backend

Install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run development server:
```
uvicorn main:app --reload
```

### frontend

Install dependencies:
```
npm install
```

Run development server:
```
npm run dev
```

## deploy

### backend

todo

The `scrape.py` needs a `config.json` for cookie management.

### frontend

```
npm run build
rsync -avzP public/* aoe2se:~/mods
```
