import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Engagement Funnel", "🔻")
df = get_filtered()
st.title("🔻 Engagement Funnel")
stages = ["Impressions", "Reach", "Likes", "Comments", "Shares", "Saves"]
vals = [df[s].sum() for s in stages]
fig = go.Figure(go.Funnel(y=stages, x=vals, textinfo="value+percent initial",
                          marker=dict(color=PALETTE + ["#607D8B"])))
fig.update_layout(title="Impressions → Reach → Likes → Comments → Shares → Saves")
st.plotly_chart(style(fig, 480), use_container_width=True)
ft = pd.DataFrame({"Stage": stages, "Total": vals})
ft["% of Impressions"] = (ft["Total"] / vals[0] * 100).round(2)
ft["% of Previous Stage"] = (ft["Total"] / ft["Total"].shift(1) * 100).round(2)
st.dataframe(ft, use_container_width=True, hide_index=True)
st.caption("Likes, comments, shares and saves are parallel actions on the same reached audience, "
           "so later stages are not a strict step-by-step drop-off.")
