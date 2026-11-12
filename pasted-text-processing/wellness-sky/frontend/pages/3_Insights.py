"""Personal trends, presented without diagnosis."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from frontend.api import call
from frontend.components import ensure_user
from frontend.design import apply_design, safety_panel

apply_design()
st.title("Your insights")
st.caption("A reflection of what you logged — not a diagnosis or a score of your wellbeing.")

if ensure_user():
    data = call("GET", "/moods/summary") or []
    if data:
        frame = pd.DataFrame(data)
        frame["day"] = pd.to_datetime(frame["day"])
        frame = frame.sort_values("day")
        figure = go.Figure(
            go.Scatter(
                x=frame["day"],
                y=frame["average"],
                mode="lines+markers",
                line={"color": "#82E4D2", "width": 3, "shape": "spline"},
                marker={"color": "#F5C96B", "size": 9, "line": {"color": "#17324D", "width": 2}},
                fill="tozeroy",
                fillcolor="rgba(130, 228, 210, .16)",
                hovertemplate="%{x|%b %-d}<br>Average mood: %{y:.1f}/5<extra></extra>",
            )
        )
        figure.update_layout(
            height=330,
            margin={"l": 10, "r": 10, "t": 20, "b": 10},
            paper_bgcolor="rgba(8, 25, 31, .76)",
            plot_bgcolor="rgba(8, 25, 31, .42)",
            font={"color": "#F4F7F1", "family": "DM Sans, sans-serif"},
            xaxis={"title": None, "showgrid": False, "fixedrange": True, "tickfont": {"color": "#D9FFF7"}},
            yaxis={"title": "Mood", "range": [1, 5], "dtick": 1, "gridcolor": "rgba(217,255,247,.25)", "fixedrange": True, "tickfont": {"color": "#D9FFF7"}, "titlefont": {"color": "#D9FFF7"}},
            hoverlabel={"bgcolor": "#17324D", "font": {"color": "#F4F7F1"}},
            showlegend=False,
        )
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False}, key="mood-trend")
        a, b = st.columns(2)
        a.metric("Check-ins", int(frame["entries"].sum()))
        b.metric("Average logged mood", f"{frame['average'].mean():.1f}/5")
        st.info("Notice a pattern that feels hard to carry? A trusted person or campus counselor can help you make sense of it.")
    else:
        st.info("Log a few check-ins to see your personal trend.")
    safety_panel()
