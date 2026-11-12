"""Streamlit entry point kept at the project root for the requested run command."""

import streamlit as st

from frontend.streamlit_app import main

st.set_page_config(page_title="Wellness Sky", page_icon="☁️", layout="wide")
main()
