"""Small, low-pressure wellbeing activities."""

import streamlit as st

from frontend.api import call
from frontend.components import ensure_user
from frontend.design import apply_design, safety_panel

apply_design()
st.title("Tiny activities")
st.caption("Choose what feels possible. Skipping is also information.")

if ensure_user():
    activities = call("GET", "/activities") or []
    for activity in activities:
        with st.container():
            left, right = st.columns([4, 1])
            with left:
                st.markdown(f"### {activity['icon']} {activity['title']}")
                st.write(activity["description"])
                st.caption(f"{activity['category']} · about {activity['minutes']} minutes")
            with right:
                if activity["completed_today"]:
                    st.success("Done today")
                elif st.button("Try it", key=f"activity-{activity['id']}"):
                    if call("POST", f"/activities/{activity['id']}/complete"):
                        st.success("Nice work.")
                        st.rerun()
            st.divider()
    safety_panel()
