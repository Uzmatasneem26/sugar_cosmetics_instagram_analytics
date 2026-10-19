import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Top 10 Engagement", "🔥")
df = get_filtered()
st.title("🔥 Top 10 Posts by Engagement Rate")
st.caption("Hidden gems: posts with high engagement relative to their reach.")
cap = max(int(df["Reach"].quantile(0.5)), 1000)
min_reach = st.slider("Minimum reach (removes tiny-reach outliers)", 0, cap, min(1000, cap), step=500)
pool = df[df["Reach"] >= min_reach]
if pool.empty:
    st.info("No posts at this minimum reach.")
else:
    top = pool.nlargest(10, "Engagement Rate").sort_values("Engagement Rate")
    fig = px.bar(top, x="Engagement Rate", y="Post Label", orientation="h",
                 text=top["Engagement Rate"].round(1).astype(str) + "%", color="Post Type",
                 color_discrete_sequence=PALETTE, title="Highest engagement rate posts")
    fig.update_yaxes(title="")
    st.plotly_chart(style(fig, 480), use_container_width=True)
    st.dataframe(top.sort_values("Engagement Rate", ascending=False)[
        ["Post ID", "Post Date", "Post Type", "Campaign Type", "Likes", "Reach", "Engagement Rate"]
    ].round(2), use_container_width=True, hide_index=True)
