# ScriptIt API

A FastAPI backend that exposes utility scripts as REST endpoints.

## Run locally

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Endpoints

### PDF
- `POST /pdf/split?start_page=1&end_page=3` — Split a PDF by page range. Accepts a PDF file upload.

### Letterboxd
- `GET /letterboxd_handler/{username}` — Get a user's watchlist
- `POST /letterboxd_handler/intersect` — Intersect watchlists from multiple users

Body example:
```json
["username1", "username2"]
```

## Adding a new script
1. Create your script in the root directory with functions only (no argparse at top level)
2. Add a router in `routers/`
3. Register it in `main.py` with `app.include_router(...)`
