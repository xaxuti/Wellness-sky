@echo off
py -c "import fastapi, streamlit" || (
  echo Wellness Sky dependencies are missing from the Python launcher.
  echo Install them with: py -m pip install -r requirements.txt
  exit /b 1
)
start "Wellness Sky API" cmd /k "py -m uvicorn backend.main:app --reload"
py -m streamlit run app.py
