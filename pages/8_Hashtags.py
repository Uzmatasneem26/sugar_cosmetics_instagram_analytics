import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Hashtags", "#️⃣")
df = get_filtered()
st.title("#️⃣ Hashtag Analysis")
hx = explode_hashtags(df)
hs = hx.groupby("Hashtag").agg(Uses=("Post ID", "count"), AvgER=("Engagement Rate", "mean"),
                               AvgReach=("Reach", "mean")).reset_index()
top_n = st.slider("Hashtags to show", 3, 20, 10)
l, r = st.columns(2)
l.plotly_chart(style(px.bar(hs.nlargest(top_n, "Uses").sort_values("Uses"), x="Uses", y="Hashtag",
                            orientation="h", title="Most Used Hashtags",
                            color_discrete_sequence=["#9C27B0"]), 400), use_container_width=True)
r.plotly_chart(style(px.bar(hs.nlargest(top_n, "AvgER").sort_values("AvgER"), x="AvgER", y="Hashtag",
                            orientation="h", title="Avg Engagement Rate (%)",
                            color_discrete_sequence=[BRAND]), 400), use_container_width=True)
st.plotly_chart(style(px.scatter(hs, x="AvgReach", y="AvgER", size="Uses", hover_name="Hashtag",
                                 title="Reach vs Engagement Rate (bubble = usage)",
                                 color_discrete_sequence=[BRAND])), use_container_width=True)
tags = df["Hashtags"].str.count(",") + 1
by_n = df.assign(Tags=tags).groupby("Tags")["Engagement Rate"].mean().reset_index()
st.plotly_chart(style(px.bar(by_n, x="Tags", y="Engagement Rate",
                             title="Avg Engagement Rate by Number of Hashtags per Post",
                             color_discrete_sequence=["#FF9800"]), 320), use_container_width=True)
st.dataframe(hs.sort_values("Uses", ascending=False).round(2), use_container_width=True, hide_index=True)
