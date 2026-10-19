import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Campaign & Growth", "🚀")
df = get_filtered()
st.title("🚀 Campaigns, Audience & Growth")
l, r = st.columns(2)
camp = df.groupby("Campaign Type")["Engagement Rate"].mean().reset_index().sort_values("Engagement Rate")
l.plotly_chart(style(px.bar(camp, x="Engagement Rate", y="Campaign Type", orientation="h",
                            title="Avg Engagement Rate by Campaign (%)", color_discrete_sequence=[BRAND])),
               use_container_width=True)
emo = df.groupby("Audience Emotion")["Engagement Rate"].mean().reset_index().sort_values("Engagement Rate")
r.plotly_chart(style(px.bar(emo, x="Engagement Rate", y="Audience Emotion", orientation="h",
                            title="Avg Engagement Rate by Audience Emotion (%)",
                            color_discrete_sequence=["#9C27B0"])), use_container_width=True)
l, r = st.columns(2)
src = df.groupby("Engagement Source")["Engagement Rate"].mean().reset_index()
l.plotly_chart(style(px.bar(src, x="Engagement Source", y="Engagement Rate",
                            text=src["Engagement Rate"].round(2), title="Avg Engagement Rate by Source (%)",
                            color_discrete_sequence=["#009688"])), use_container_width=True)
conv = df.groupby("Post Type").agg(V=("Profile Visits", "sum"), F=("Follows", "sum")).reset_index()
conv["Follow Conversion %"] = conv["F"] / conv["V"] * 100
r.plotly_chart(style(px.bar(conv, x="Post Type", y="Follow Conversion %",
                            text=conv["Follow Conversion %"].round(1),
                            title="Profile Visit → Follow Conversion (%)",
                            color_discrete_sequence=["#3F51B5"])), use_container_width=True)
g = df.groupby("Month")["Follows"].sum().reset_index()
g["Cumulative Follows"] = g["Follows"].cumsum()
fig = px.area(g, x="Month", y="Cumulative Follows", title="Cumulative New Follows",
              color_discrete_sequence=[BRAND])
fig.update_xaxes(dtick="M1", tickformat="%b %Y")
st.plotly_chart(style(fig, 350), use_container_width=True)
