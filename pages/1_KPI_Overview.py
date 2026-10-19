import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("KPI Overview", "📊")
df = get_filtered()
st.title("📊 KPI Overview")
st.caption("How is the overall account performing?")
c = st.columns(5)
c[0].metric("Total Posts", f"{len(df):,}")
c[1].metric("Total Likes", fmt(df["Likes"].sum()))
c[2].metric("Total Comments", fmt(df["Comments"].sum()))
c[3].metric("Total Reach", fmt(df["Reach"].sum()))
c[4].metric("Avg Engagement Rate", f"{df['Engagement Rate'].mean():.2f}%")
c = st.columns(5)
c[0].metric("Impressions", fmt(df["Impressions"].sum()))
c[1].metric("Shares", fmt(df["Shares"].sum()))
c[2].metric("Saves", fmt(df["Saves"].sum()))
c[3].metric("Profile Visits", fmt(df["Profile Visits"].sum()))
c[4].metric("New Follows", fmt(df["Follows"].sum()))
st.caption("Engagement Rate = (Likes + Comments + Shares + Saves) / Reach × 100, per post, then averaged.")
l, r = st.columns(2)
mix = df["Post Type"].value_counts().reset_index()
l.plotly_chart(style(px.pie(mix, names="Post Type", values="count", hole=0.5, title="Post Mix by Format",
                            color_discrete_sequence=PALETTE)), use_container_width=True)
wtd = df["Total Engagement"].sum() / df["Reach"].sum() * 100
r.plotly_chart(style(px.histogram(df, x="Engagement Rate", nbins=50, color_discrete_sequence=[BRAND],
                                  title=f"Engagement Rate Distribution (weighted overall {wtd:.2f}%)")),
               use_container_width=True)
