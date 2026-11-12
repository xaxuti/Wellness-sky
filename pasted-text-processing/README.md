# Wellness Sky

Wellness Sky is a privacy-first Student Mental Wellness Platform. The repository
now contains only the requested Streamlit + FastAPI application in
[`wellness-sky/`](wellness-sky/).

## Quick start

```bash
cd wellness-sky
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py

# terminal 1
uvicorn backend.main:app --reload

# terminal 2
streamlit run frontend/streamlit_app.py
```

The app is a wellbeing companion, not a medical diagnosis or crisis service.
Use the Safety page for immediate support options.
# Wellness-sky
