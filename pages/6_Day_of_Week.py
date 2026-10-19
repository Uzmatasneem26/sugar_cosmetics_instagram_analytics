import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Day of Week", "📅")
df = get_filtered()
st.title("📅 Day of Week Analysis")
dw = df.groupby("Weekday", observed=False).agg(Posts=("Post ID", "count"), ER=("Engagement Rate", "mean")).reset_index()
l, r = st.columns(2)
l.plotly_chart(style(px.bar(dw, x="Weekday", y="ER", text=dw["ER"].round(2),
                            title="Avg Engagement Rate by Weekday (%)", color_discrete_sequence=[BRAND])),
               use_container_width=True)
r.plotly_chart(style(px.bar(dw, x="Weekday", y="Posts", title="Posting Volume by Weekday",
                            color_discrete_sequence=["#9C27B0"])), use_container_width=True)
heat = df.groupby(["Weekday", "Post Type"], observed=False)["Engagement Rate"].mean().reset_index()
heat = heat.pivot(index="Post Type", columns="Weekday", values="Engagement Rate")
st.plotly_chart(style(px.imshow(heat, text_auto=".2f", aspect="auto", color_continuous_scale="RdPu",
                                title="Engagement Rate: Weekday × Post Type"), 320), use_container_width=True)
