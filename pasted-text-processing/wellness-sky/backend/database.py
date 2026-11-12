"""Small, dependency-light SQLite data layer."""

from contextlib import contextmanager
import sqlite3
from typing import Iterator

from .config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
    label TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '',
    reflection TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_moods_user_created ON moods(user_id, created_at);
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    minutes INTEGER NOT NULL DEFAULT 5,
    icon TEXT NOT NULL DEFAULT '🌱'
);
CREATE TABLE IF NOT EXISTS activity_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ciphertext TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    theme TEXT NOT NULL DEFAULT 'Sky',
    reminders INTEGER NOT NULL DEFAULT 1,
    anonymous_analytics INTEGER NOT NULL DEFAULT 0
);
"""


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    """Yield a foreign-key-enabled connection and commit successful work."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connection() as conn:
        conn.executescript(SCHEMA)


def seed_db() -> None:
    init_db()
    activities = [
        ("Two-minute reset", "Unclench your jaw, drop your shoulders, and take five slow breaths.", "Mindful pause", 2, "🌬️"),
        ("Name five things", "Look around and name five things you can see, four you can feel, and three you can hear.", "Grounding", 5, "🪨"),
        ("Tiny outside break", "Step outside or look through a window. Notice one color, one sound, and one temperature.", "Movement", 10, "🌤️"),
        ("Kind note to self", "Write one sentence you would say to a friend having the same day you are having.", "Reflection", 5, "💌"),
        ("Study reset", "Pick one next action, set a ten-minute timer, and begin without aiming for perfect.", "Focus", 10, "📚"),
        ("Box breathing", "Breathe in, hold, breathe out, hold — four counts each, for five rounds.", "Breathing", 4, "🫧"),
        ("Long exhale", "Inhale gently for four counts, then exhale for six. Repeat until your shoulders soften.", "Breathing", 3, "🌬️"),
        ("Body scan", "Notice your feet, legs, belly, shoulders, jaw, and forehead without needing to change anything.", "Meditation", 8, "🧘"),
        ("Shoulder release", "Circle your shoulders slowly, stretch your neck, and shake out your hands.", "Stretching", 5, "🙆"),
        ("Three-line journal", "Write what happened, how it felt, and one kind next step.", "Journaling", 5, "✍️"),
        ("Sleep landing", "Dim the lights, put your phone down, and name three things you can leave for tomorrow.", "Sleep", 10, "🌙"),
        ("Exam pressure pause", "Choose the smallest useful study action and pair it with one minute of steady breathing.", "Exam support", 6, "📖"),
    ]
    with connection() as conn:
        if conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO activities(title, description, category, minutes, icon) VALUES (?, ?, ?, ?, ?)",
                activities,
            )
