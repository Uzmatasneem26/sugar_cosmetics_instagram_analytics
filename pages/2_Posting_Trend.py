import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Posting Trend", "📈")
df = get_filtered()
st.title("📈 Monthly Posting Trend")
m = df.groupby("Month").agg(Posts=("Post ID", "count"), AvgER=("Engagement Rate", "mean")).reset_index()
fig = px.line(m, x="Month", y="Posts", markers=True, title="Posts per Month", color_discrete_sequence=[BRAND])
fig.update_xaxes(dtick="M1", tickformat="%b %Y")
st.plotly_chart(style(fig), use_container_width=True)
fig2 = px.line(m, x="Month", y="AvgER", markers=True, title="Average Engagement Rate by Month (%)",
               color_discrete_sequence=["#9C27B0"])
fig2.update_xaxes(dtick="M1", tickformat="%b %Y")
st.plotly_chart(style(fig2, 350), use_container_width=True)
st.caption("The first and last months are partial in the data window, so they look lower.")
