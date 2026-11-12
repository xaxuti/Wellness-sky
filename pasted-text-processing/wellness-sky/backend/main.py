"""FastAPI application for Wellness Sky."""

from datetime import datetime, timezone
import json
import sqlite3
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status

from .database import connection, seed_db
from .models import (
    ActivityResponse, AuthResponse, LoginRequest, MoodCreate, MoodResponse,
    NoteCreate, NoteResponse, Preferences, RegisterRequest, UserResponse,
)
from .security import (
    create_token, decrypt_note, encrypt_note, hash_password, read_token,
    verify_password,
)
from .config import DATA_DIR

app = FastAPI(title="Wellness Sky API", version="1.0.0")
seed_db()


def _as_dict(row) -> dict:
    return {key: row[key] for key in row.keys()}


def _user_row(user_id: int):
    with connection() as conn:
        return conn.execute("SELECT id, email, name FROM users WHERE id=?", (user_id,)).fetchone()


def current_user(authorization: str = Header(default="")):
    scheme, _, token = authorization.partition(" ")
    user_id = read_token(token) if scheme.lower() == "bearer" else None
    user = _user_row(user_id) if user_id else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in to continue")
    return user


@app.get("/health")
def health():
    return {"status": "ok", "service": "wellness-sky"}


@app.post("/auth/register", response_model=AuthResponse, status_code=201)
def register(body: RegisterRequest):
    try:
        with connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users(email, name, password_hash) VALUES (?, ?, ?)",
                (body.email.strip().lower(), body.name.strip(), hash_password(body.password)),
            )
            user_id = cursor.lastrowid
            conn.execute("INSERT INTO preferences(user_id) VALUES (?)", (user_id,))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="An account with that email already exists")
    user = _user_row(user_id)
    return {"token": create_token(user_id), "user": _as_dict(user)}


@app.post("/auth/login", response_model=AuthResponse)
def login(body: LoginRequest):
    with connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE email=?", (body.email.strip().lower(),)).fetchone()
    if user is None or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email or password is not correct")
    return {"token": create_token(user["id"]), "user": {"id": user["id"], "email": user["email"], "name": user["name"]}}


@app.get("/me", response_model=UserResponse)
def me(user=Depends(current_user)):
    return _as_dict(user)


def _mood(row) -> dict:
    item = _as_dict(row)
    item["tags"] = json.loads(item.pop("tags") or "[]")
    return item


@app.get("/moods", response_model=List[MoodResponse])
def list_moods(limit: int = Query(default=30, ge=1, le=365), user=Depends(current_user)):
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, score, label, tags, reflection, created_at FROM moods WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
            (user["id"], limit),
        ).fetchall()
    return [_mood(row) for row in rows]


@app.post("/moods", response_model=MoodResponse, status_code=201)
def create_mood(body: MoodCreate, user=Depends(current_user)):
    with connection() as conn:
        cursor = conn.execute(
            "INSERT INTO moods(user_id, score, label, tags, reflection) VALUES (?, ?, ?, ?, ?)",
            (user["id"], body.score, body.label.strip(), json.dumps(body.tags), body.reflection.strip()),
        )
        row = conn.execute("SELECT id, score, label, tags, reflection, created_at FROM moods WHERE id=?", (cursor.lastrowid,)).fetchone()
    return _mood(row)


@app.put("/moods/{mood_id}", response_model=MoodResponse)
def update_mood(mood_id: int, body: MoodCreate, user=Depends(current_user)):
    with connection() as conn:
        cursor = conn.execute(
            "UPDATE moods SET score=?, label=?, tags=?, reflection=? WHERE id=? AND user_id=?",
            (body.score, body.label.strip(), json.dumps(body.tags), body.reflection.strip(), mood_id, user["id"]),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        row = conn.execute("SELECT id, score, label, tags, reflection, created_at FROM moods WHERE id=?", (mood_id,)).fetchone()
    return _mood(row)


@app.delete("/moods/{mood_id}", status_code=204)
def delete_mood(mood_id: int, user=Depends(current_user)):
    with connection() as conn:
        cursor = conn.execute("DELETE FROM moods WHERE id=? AND user_id=?", (mood_id, user["id"]))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Mood entry not found")


@app.get("/moods/summary")
def mood_summary(user=Depends(current_user)):
    with connection() as conn:
        rows = conn.execute(
            "SELECT date(created_at) day, ROUND(AVG(score), 2) average, COUNT(*) entries FROM moods WHERE user_id=? GROUP BY day ORDER BY day",
            (user["id"],),
        ).fetchall()
    return [_as_dict(row) for row in rows]


@app.get("/activities", response_model=List[ActivityResponse])
def activities(user=Depends(current_user)):
    with connection() as conn:
        rows = conn.execute(
            """SELECT a.*, EXISTS(SELECT 1 FROM activity_completions c
               WHERE c.activity_id=a.id AND c.user_id=? AND date(c.completed_at)=date('now')) completed_today
               FROM activities a ORDER BY a.category, a.id""", (user["id"],)
        ).fetchall()
    return [_as_dict(row) for row in rows]


@app.post("/activities/{activity_id}/complete")
def complete_activity(activity_id: int, user=Depends(current_user)):
    with connection() as conn:
        exists = conn.execute("SELECT id FROM activities WHERE id=?", (activity_id,)).fetchone()
        if exists is None:
            raise HTTPException(status_code=404, detail="Activity not found")
        conn.execute("INSERT INTO activity_completions(user_id, activity_id) VALUES (?, ?)", (user["id"], activity_id))
    return {"completed": True, "activity_id": activity_id}


@app.get("/notes", response_model=List[NoteResponse])
def notes(user=Depends(current_user)):
    with connection() as conn:
        rows = conn.execute("SELECT * FROM notes WHERE user_id=? ORDER BY updated_at DESC", (user["id"],)).fetchall()
    return [{**_as_dict(row), "text": decrypt_note(row["ciphertext"])} for row in rows]


@app.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(body: NoteCreate, user=Depends(current_user)):
    with connection() as conn:
        cursor = conn.execute("INSERT INTO notes(user_id, ciphertext) VALUES (?, ?)", (user["id"], encrypt_note(body.text)))
        row = conn.execute("SELECT * FROM notes WHERE id=?", (cursor.lastrowid,)).fetchone()
    return {**_as_dict(row), "text": body.text}


@app.get("/resources")
def resources():
    with (DATA_DIR / "resources.json").open(encoding="utf-8") as resource_file:
        return json.load(resource_file)


@app.get("/preferences", response_model=Preferences)
def get_preferences(user=Depends(current_user)):
    with connection() as conn:
        row = conn.execute("SELECT theme, reminders, anonymous_analytics FROM preferences WHERE user_id=?", (user["id"],)).fetchone()
    return {"theme": row["theme"], "reminders": bool(row["reminders"]), "anonymous_analytics": bool(row["anonymous_analytics"])}


@app.put("/preferences", response_model=Preferences)
def update_preferences(body: Preferences, user=Depends(current_user)):
    with connection() as conn:
        conn.execute(
            """INSERT INTO preferences(user_id, theme, reminders, anonymous_analytics) VALUES (?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET theme=excluded.theme, reminders=excluded.reminders,
               anonymous_analytics=excluded.anonymous_analytics""",
            (user["id"], body.theme, int(body.reminders), int(body.anonymous_analytics)),
        )
    return body
