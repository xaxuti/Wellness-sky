"""Support resources and safety guidance."""

import streamlit as st

from frontend.api import call
from frontend.design import apply_design, safety_panel

apply_design()
st.title("Support & resources")
st.markdown("You deserve support before things become an emergency.")
st.error("If you may hurt yourself or someone else, call local emergency services now. In the US or Canada, call or text 988.")

resources = call("GET", "/resources") or []
for resource in resources:
    tone = "urgent" if resource.get("urgent") else "resource"
    with st.container():
        st.markdown(f"### {resource['name']}")
        st.write(resource["description"])
        st.link_button("Open resource", resource["url"])
        st.divider()
safety_panel()
