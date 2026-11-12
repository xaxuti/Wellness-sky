"""Account, privacy, and display settings."""

import json
import streamlit as st

from frontend.api import call, sign_out
from frontend.components import ensure_user
from frontend.design import apply_design

apply_design()
st.title("Settings")
if ensure_user():
    preferences = call("GET", "/preferences") or {}
    with st.form("preferences"):
        themes = ["Sky", "Lavender", "Amber"]
        saved_theme = "Amber" if preferences.get("theme", "Sky") == "High contrast" else preferences.get("theme", "Sky")
        theme = st.selectbox("Visual theme", themes, index=themes.index(saved_theme) if saved_theme in themes else 0)
        reminders = st.toggle("Gentle reminders", value=preferences.get("reminders", True))
        sound = st.toggle("Play optional tiny chimes", value=st.session_state.get("sound_enabled", True))
        if st.form_submit_button("Save settings", type="primary"):
            if call("PUT", "/preferences", json={"theme": theme, "reminders": reminders, "anonymous_analytics": False}):
                st.session_state.theme = theme
                st.session_state.sound_enabled = sound
                st.success("Settings saved.")
    st.divider()
    st.subheader("Your data")
    st.caption("Export the check-ins currently stored on your account.")
    moods = call("GET", "/moods?limit=365") or []
    st.download_button("Download mood journal (JSON)", json.dumps(moods, indent=2), "wellness-sky-moods.json", "application/json")
    st.info("To request account deletion, contact the person operating this deployment. Never share your password.")
