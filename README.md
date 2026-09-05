# YaCut

URL shortener on Flask with asynchronous multi-file upload to Yandex Disk.

Built during the *Python Developer* course at Yandex Practicum (2025–2026). Every project was reviewed and accepted by a course mentor. Final project of the module *Asynchronous Python and Flask*.

## Features

- Shorten a long URL to a random or custom short id, redirect on visit
- Upload several files at once; the files are sent to Yandex Disk **concurrently** with `asyncio` + `aiohttp`, and a short link is created for every uploaded file
- JSON API with validation and custom error handlers
- OpenAPI specification (`openapi.yml`) and a Postman collection

## Tech stack

Python 3 · Flask · Flask-SQLAlchemy · WTForms · asyncio · aiohttp · SQLite · pytest

## API

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/id/` | create a short link — `{"url": "...", "custom_id": "..."}` |
| `GET` | `/api/id/<short_id>/` | resolve a short id to the original URL |

## Run locally

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```text
FLASK_APP=yacut
SECRET_KEY=replace-with-a-secret-key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your-yandex-disk-oauth-token
```

```bash
flask shell -c "from yacut import db; db.create_all()"
flask run
```

## Tests

```bash
pytest          # 35 tests
flake8 yacut config.py
```

## Author

Roman Tanashkin — [github.com/RomanTanashkin](https://github.com/RomanTanashkin)
