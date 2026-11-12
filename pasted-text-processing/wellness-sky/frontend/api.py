"""Tiny API client used by all Streamlit pages."""

import os
from typing import Any, Dict, Optional

import requests

API_URL = os.getenv("WELLNESS_API_URL", "http://127.0.0.1:8000")


def _headers() -> Dict[str, str]:
    token = __import__("streamlit").session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def call(method: str, path: str, **kwargs: Any) -> Optional[Any]:
    import streamlit as st

    try:
        response = requests.request(method, API_URL + path, headers=_headers(), timeout=4, **kwargs)
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.reason)
            except ValueError:
                detail = response.reason
            st.session_state.api_error = str(detail)
            return None
        st.session_state.pop("api_error", None)
        return response.json() if response.content else {}
    except requests.RequestException as exc:
        st.session_state.api_error = f"API unavailable at {API_URL}: {exc}"
        return None


def sign_in(email: str, password: str, register: bool = False, name: str = "") -> Optional[dict]:
    payload = {"email": email, "password": password}
    if register:
        payload["name"] = name
    return call("POST", "/auth/register" if register else "/auth/login", json=payload)


def sign_out() -> None:
    import streamlit as st
    st.session_state.pop("token", None)
    st.session_state.pop("user", None)
