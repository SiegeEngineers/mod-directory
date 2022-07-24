# mod-directory

An overview over mods on the mod center


## develop

### frontend

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

### backend

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

### frontend

```
npm run build
rsync -avzP public/* aoe2se:~/mods
```
