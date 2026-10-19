import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Post Types", "🎞️")
df = get_filtered()
st.title("🎞️ Post Type Performance")
pt = df.groupby("Post Type").agg(Posts=("Post ID", "count"), Likes=("Likes", "mean"), Comments=("Comments", "mean"),
                                 Shares=("Shares", "mean"), Saves=("Saves", "mean"), Reach=("Reach", "mean"),
                                 ER=("Engagement Rate", "mean")).reset_index()
long = pt.melt(id_vars="Post Type", value_vars=["Likes", "Comments", "Shares", "Saves"],
               var_name="Metric", value_name="Average")
st.plotly_chart(style(px.bar(long, x="Post Type", y="Average", color="Metric", barmode="group",
                             title="Average Likes, Comments, Shares & Saves per Post",
                             color_discrete_sequence=PALETTE)), use_container_width=True)
l, r = st.columns(2)
l.plotly_chart(style(px.bar(pt, x="Post Type", y="ER", text=pt["ER"].round(2), title="Avg Engagement Rate (%)",
                            color_discrete_sequence=[BRAND])), use_container_width=True)
r.plotly_chart(style(px.bar(pt, x="Post Type", y="Reach", text=pt["Reach"].round(0), title="Avg Reach per Post",
                            color_discrete_sequence=["#3F51B5"])), use_container_width=True)
st.dataframe(pt.round(2), use_container_width=True, hide_index=True)
