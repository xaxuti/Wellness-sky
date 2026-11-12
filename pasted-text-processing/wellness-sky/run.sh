#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -c "import fastapi, streamlit" 2>/dev/null || {
  echo "Wellness Sky dependencies are missing from $PYTHON_BIN."
  echo "Install them with: $PYTHON_BIN -m pip install -r requirements.txt"
  exit 1
}

"$PYTHON_BIN" -m uvicorn backend.main:app --reload &
api_pid=$!
trap 'kill "$api_pid"' EXIT
"$PYTHON_BIN" -m streamlit run app.py
