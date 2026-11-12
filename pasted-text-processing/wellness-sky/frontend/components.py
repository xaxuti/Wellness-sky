"""Reusable Streamlit components."""

import streamlit as st

from .api import call
from .design import safety_panel


def ensure_user() -> bool:
    if st.session_state.get("token"):
        return True
    st.warning("Sign in from the home page to save your wellness check-ins.")
    safety_panel()
    return False


def render_mood_form() -> None:
    st.subheader("How are you feeling?")
    labels = ["Very low", "Low", "Okay", "Good", "Bright"]
    with st.form("mood_form", clear_on_submit=True):
        score = st.slider("Mood", 1, 5, 3, format="%d/5")
        st.caption(labels[score - 1])
        label_choice = st.selectbox(
            "A word for it",
            ["Calm", "Anxious", "Tired", "Focused", "Hopeful", "Type your own"],
        )
        custom_label = st.text_input(
            "Or type your own",
            max_chars=32,
            placeholder="Type a word and press Enter",
        )
        label = custom_label.strip() or ("" if label_choice == "Type your own" else label_choice)
        tag_options = ["study", "sleep", "friends", "family", "body", "money", "future", "Type your own"]
        selected_tags = st.multiselect("What is part of the picture?", tag_options)
        tags = [tag for tag in selected_tags if tag != "Type your own"]
        custom_tags = st.text_input(
            "Or type your own tags",
            placeholder="Type tags separated by commas and press Enter",
            max_chars=80,
        )
        if custom_tags.strip():
            tags.extend(tag.strip().lower() for tag in custom_tags.split(",") if tag.strip())
        reflection = st.text_area("Optional reflection", placeholder="A sentence is enough.")
        if st.form_submit_button("Save check-in", type="primary"):
            if not label.strip():
                st.error("Add a word for how you are feeling.")
                return
            result = call("POST", "/moods", json={"score": score, "label": label, "tags": tags, "reflection": reflection})
            if result:
                st.success("Check-in saved. Thank you for noticing how you are doing.")
                st.rerun()
            else:
                st.error("Could not save this check-in. Is the API running?")
