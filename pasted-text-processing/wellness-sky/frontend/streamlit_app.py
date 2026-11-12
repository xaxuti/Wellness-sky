"""Wellness Sky Streamlit dashboard."""

import streamlit as st

from frontend.api import call, sign_in, sign_out
from frontend.components import render_mood_form
from frontend.design import apply_design, music_moment, safety_panel

def auth_box() -> None:
    st.subheader("Welcome to your softer corner of the internet.")
    st.write("Sign in to keep check-ins private, or create a local account to get started.")
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Sign in"
    mode = st.session_state.auth_mode
    with st.form("auth"):
        name = st.text_input("Name") if mode == "Create account" else ""
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", help="At least 8 characters")
        if st.form_submit_button(mode, type="primary", use_container_width=True):
            if mode == "Create account" and len(password) < 8:
                st.error("Use at least 8 characters for your password.")
                return
            result = sign_in(email, password, mode == "Create account", name)
            if result:
                st.session_state.token, st.session_state.user = result["token"], result["user"]
                st.rerun()
            else:
                st.error(
                    st.session_state.get(
                        "api_error",
                        "We could not complete that request. Check your details and that the API is running.",
                    )
                )
    switch_label = "Already have an account? Sign in" if mode == "Create account" else "New here? Create an account"
    if st.button(switch_label, key="auth-switch", type="secondary"):
        st.session_state.auth_mode = "Sign in" if mode == "Create account" else "Create account"
        st.rerun()


def dashboard() -> None:
    user = st.session_state.get("user", {})
    st.markdown(
        f'<div class="hero"><div class="eyebrow">Good to see you</div><h1>Hi {user.get("name", "there")} ☁️</h1>'
        "<p>You do not have to solve everything today. One small check-in is enough.</p></div>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1.5, 1])
    with col1:
        render_mood_form()
    with col2:
        st.markdown('<div class="card"><div class="eyebrow">A gentle next step</div><h3>Try a two-minute reset</h3>'
                    "<p>Drop your shoulders and take five slow breaths. Notice what changes, without judging it.</p></div>",
                    unsafe_allow_html=True)
        st.write("")
        safety_panel()
    moods = call("GET", "/moods?limit=5") or []
    if moods:
        st.subheader("Recent check-ins")
        for item in moods:
            st.markdown(f"**{item['label']}** · {item['score']}/5 · {item['created_at'][:10]}")
            if item.get("reflection"):
                st.caption(item["reflection"])


def main() -> None:
    if st.session_state.get("token") and "theme" not in st.session_state:
        preferences = call("GET", "/preferences") or {}
        saved_theme = preferences.get("theme", "Sky")
        st.session_state.theme = "Amber" if saved_theme == "High contrast" else saved_theme
        st.session_state.sound_enabled = preferences.get("sound_enabled", True)
    apply_design()
    if not st.session_state.get("token"):
        st.markdown(
            '<div class="hero"><div class="eyebrow">Student mental wellness</div>'
            '<h1>Make a little room for yourself.</h1>'
            "<p>Wellness Sky helps you notice patterns, practice tiny resets, and "
            "find support when you need it.</p></div>",
            unsafe_allow_html=True,
        )
        auth_box()
    else:
        with st.sidebar:
            st.markdown("## ☁️ Wellness Sky")
            st.caption("A private space for small steps.")
            music_moment()
            if st.button("Sign out"):
                sign_out()
                st.rerun()

        pages = [
            st.Page(dashboard, title="Today", icon="☁️", default=True),
            st.Page("frontend/pages/1_Mood_Journal.py", title="Mood journal", icon="📝"),
            st.Page("frontend/pages/2_Activities.py", title="Activities", icon="🌱"),
            st.Page("frontend/pages/3_Insights.py", title="Insights", icon="✨"),
            st.Page("frontend/pages/4_Resources.py", title="Resources", icon="🧭"),
            st.Page("frontend/pages/5_Settings.py", title="Settings", icon="⚙️"),
        ]
        navigation = st.navigation(pages)
        navigation.run()
