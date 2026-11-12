"""Typed response models used by the API."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class RegisterRequest(BaseModel):
    email: str
    name: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


class MoodCreate(BaseModel):
    score: int = Field(ge=1, le=5)
    label: str = Field(min_length=1, max_length=32)
    tags: List[str] = Field(default_factory=list)
    reflection: str = Field(default="", max_length=500)

    @validator("tags")
    def clean_tags(cls, value):
        return [tag.strip().lower() for tag in value if tag.strip()][:8]


class MoodResponse(MoodCreate):
    id: int
    created_at: datetime


class ActivityResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    minutes: int
    icon: str
    completed_today: bool = False


class NoteCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class NoteResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    updated_at: datetime


class Preferences(BaseModel):
    theme: str = "Sky"
    reminders: bool = True
    anonymous_analytics: bool = False
