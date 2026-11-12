# Architecture

`backend/main.py` exposes an authenticated FastAPI JSON API. `backend/database.py`
owns the SQLite schema and uses parameterized queries. Passwords use PBKDF2
with a per-user salt; journal notes use Fernet authenticated encryption before
being written to SQLite. Signed bearer tokens expire after the configured TTL.

`frontend/streamlit_app.py` is the dashboard entry point. Streamlit discovers
the pages in `frontend/pages/`, while `frontend/api.py` keeps HTTP details out
of presentation code. The frontend shows a helpful sign-in prompt when the API
is not running instead of silently inventing wellness data.
