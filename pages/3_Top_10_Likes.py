import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Top 10 Likes", "❤️")
df = get_filtered()
st.title("❤️ Top 10 Posts by Likes")
st.caption("The dataset has no caption column, so posts are identified by ID, format, campaign and date.")
top = df.nlargest(10, "Likes").sort_values("Likes")
fig = px.bar(top, x="Likes", y="Post Label", orientation="h", text="Likes", color="Post Type",
             color_discrete_sequence=PALETTE, title="Most-liked posts")
fig.update_yaxes(title="")
st.plotly_chart(style(fig, 480), use_container_width=True)
st.dataframe(top.sort_values("Likes", ascending=False)[
    ["Post ID", "Post Date", "Post Type", "Campaign Type", "Hashtags", "Likes", "Reach", "Engagement Rate"]
].round(2), use_container_width=True, hide_index=True)
