"""Password and session helpers without storing plaintext secrets."""

import base64
import binascii
import hashlib
import hmac
import json
import secrets
import time
from typing import Dict, Optional

from cryptography.fernet import Fernet, InvalidToken

from .config import SECRET_KEY, TOKEN_TTL_HOURS


def hash_password(password: str, salt: Optional[bytes] = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240_000)
    return "pbkdf2$%s$%s" % (
        base64.urlsafe_b64encode(salt).decode(),
        base64.urlsafe_b64encode(digest).decode(),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, salt, expected = encoded.split("$")
        actual = hash_password(password, base64.urlsafe_b64decode(salt)).split("$")[-1]
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _signing_key() -> bytes:
    return hashlib.sha256(SECRET_KEY.encode()).digest()


def create_token(user_id: int) -> str:
    payload = {"sub": user_id, "exp": int(time.time()) + TOKEN_TTL_HOURS * 3600}
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = hmac.new(_signing_key(), encoded.encode(), hashlib.sha256).hexdigest()
    return encoded + "." + signature


def read_token(token: str) -> Optional[int]:
    try:
        encoded, signature = token.split(".", 1)
        expected = hmac.new(_signing_key(), encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        if int(payload["exp"]) < int(time.time()):
            return None
        return int(payload["sub"])
    except (ValueError, KeyError, TypeError, binascii.Error, json.JSONDecodeError):
        return None


def _fernet() -> Fernet:
    key = base64.urlsafe_b64encode(_signing_key())
    return Fernet(key)


def encrypt_note(text: str) -> str:
    return _fernet().encrypt(text.encode()).decode()


def decrypt_note(ciphertext: str) -> str:
    try:
        return _fernet().decrypt(ciphertext.encode()).decode()
    except (InvalidToken, UnicodeDecodeError):
        return "[This note could not be decrypted]"
