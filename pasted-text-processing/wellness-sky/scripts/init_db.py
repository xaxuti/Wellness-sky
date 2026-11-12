"""Create the local database and safe starter content."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.database import seed_db

if __name__ == "__main__":
    seed_db()
    print("Wellness Sky database is ready.")
