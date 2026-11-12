"""Mood history and private encrypted notes."""

import streamlit as st

from frontend.api import call
from frontend.components import ensure_user
from frontend.design import apply_design, safety_panel

apply_design()
st.title("Mood journal")
st.caption("Patterns, not judgments. You can edit or delete any check-in.")

if ensure_user():
    moods = call("GET", "/moods?limit=100") or []
    if moods:
        for mood in moods:
            with st.expander(f"{mood['created_at'][:10]} · {mood['label']} · {mood['score']}/5"):
                st.write(mood.get("reflection") or "No reflection added.")
                st.caption(" ".join("#" + tag for tag in mood.get("tags", [])))
                if st.button("Delete", key=f"delete-{mood['id']}"):
                    call("DELETE", f"/moods/{mood['id']}")
                    st.rerun()
    else:
        st.info("Your first check-in will appear here.")
    st.divider()
    st.subheader("Private notes")
    st.caption("Notes are encrypted before they are stored.")
    with st.form("note"):
        text = st.text_area("Write freely", height=140)
        if st.form_submit_button("Save private note"):
            if text.strip() and call("POST", "/notes", json={"text": text}):
                st.success("Your note was encrypted and saved.")
                st.rerun()
    for note in call("GET", "/notes") or []:
        st.markdown(f"**{note['updated_at'][:10]}**")
        st.write(note["text"])
    safety_panel()
