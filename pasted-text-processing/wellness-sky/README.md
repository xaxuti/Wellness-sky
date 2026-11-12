# Wellness Sky

An approachable, student-first mental wellness companion with a FastAPI
backend and a Streamlit multipage interface. The default database is SQLite,
and private journal notes are encrypted before they are stored.

## Features

- account registration and signed bearer sessions
- mood CRUD with optional tags and reflections
- activity library and completion tracking
- trend summaries and charts
- encrypted private notes
- curated, local resources and an always-visible safety panel
- settings for display preferences, data export, and account deletion

This product supports reflection and habit building. It does not diagnose,
treat, or replace a qualified professional.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python scripts/init_db.py
./run.sh
```

Set `WELLNESS_SECRET_KEY` in production. The development default is
deliberately local-only and should not be reused.

Use the same interpreter for installation and launch. If your machine has
multiple Python environments, set `PYTHON_BIN` before running the launcher:

```bash
PYTHON_BIN=/path/to/python ./run.sh
```

Run each command separately. Do not join `./run.sh` and the next `cd` command
on the same line. If pip reports a Rust build failure for an unrelated package
such as `libcst`, confirm the active environment with `which python` and
`python -m pip --version`; both should point inside `.venv`.
