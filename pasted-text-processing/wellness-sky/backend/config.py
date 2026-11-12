"""Environment-backed settings with safe local defaults."""

from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_PATH = Path(os.getenv("WELLNESS_DATABASE", str(DATA_DIR / "wellness.db")))
SECRET_KEY = os.getenv(
    "WELLNESS_SECRET_KEY",
    "development-only-change-me-please-32-characters",
)
TOKEN_TTL_HOURS = int(os.getenv("WELLNESS_TOKEN_TTL_HOURS", "168"))
APP_NAME = "Wellness Sky"
