"""Shared data loading, filters and styling for all pages."""
from pathlib import Path

import pandas as pd
import streamlit as st

BRAND = "#E91E63"
PALETTE = ["#E91E63", "#9C27B0", "#FF9800", "#3F51B5", "#009688", "#795548"]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DATA_FILE = Path(__file__).parent / "sugar_cosmetics_instagram_data.xlsx"


def setup(title: str, icon: str = "💄"):
    st.set_page_config(page_title=f"{title} | Sugar Cosmetics", page_icon=icon, layout="wide")
    st.markdown(
        """<style>
        div[data-testid="stMetric"] {background:#fff5f8; border:1px solid #f8bbd0;
            padding:14px 16px; border-radius:12px;}
        h1, h2, h3 {color:#880e4f;}
        </style>""",
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner="Loading data...")
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_FILE)
    df.columns = [c.strip() for c in df.columns]
    df["Post Date"] = pd.to_datetime(df["Post Date"], errors="coerce")
    df = df.dropna(subset=["Post Date"]).drop_duplicates().reset_index(drop=True)
    df.insert(0, "Post ID", df.index + 1)
    nums = ["Impressions", "Reach", "Likes", "Comments", "Shares", "Saves", "Profile Visits", "Follows"]
    df[nums] = df[nums].apply(pd.to_numeric, errors="coerce").fillna(0)
    df = df[df["Reach"] > 0].copy()
    df["Total Engagement"] = df[["Likes", "Comments", "Shares", "Saves"]].sum(axis=1)
    df["Engagement Rate"] = df["Total Engagement"] / df["Reach"] * 100
    df["Month"] = df["Post Date"].dt.to_period("M").dt.to_timestamp()
    df["Weekday"] = pd.Categorical(df["Post Date"].dt.day_name(), DAY_ORDER, ordered=True)
    df["Post Label"] = ("#" + df["Post ID"].astype(str) + " | " + df["Post Type"] + " | "
                        + df["Campaign Type"] + " | " + df["Post Date"].dt.strftime("%d %b %Y"))
    return df


@st.cache_data
def explode_hashtags(df: pd.DataFrame) -> pd.DataFrame:
    h = df.assign(Hashtag=df["Hashtags"].fillna("").str.split(r",\s*")).explode("Hashtag")
    h["Hashtag"] = h["Hashtag"].str.strip()
    return h[h["Hashtag"] != ""]


def fmt(n: float) -> str:
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(n) >= div:
            return f"{n / div:.2f}{unit}"
    return f"{n:,.0f}"


def style(fig, height=420):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=50, b=10),
                      template="plotly_white", legend_title_text="")
    return fig


def get_filtered(show_filters: bool = True) -> pd.DataFrame:
    """Sidebar filters shared by every page (selections persist across pages)."""
    raw = load_data()
    opts = {
        "f_type": sorted(raw["Post Type"].unique()),
        "f_camp": sorted(raw["Campaign Type"].unique()),
        "f_src": sorted(raw["Engagement Source"].unique()),
        "f_emo": sorted(raw["Audience Emotion"].unique()),
    }
    dmin, dmax = raw["Post Date"].min().date(), raw["Post Date"].max().date()
    st.session_state.setdefault("f_date", (dmin, dmax))
    for k, v in opts.items():
        st.session_state.setdefault(k, v)
    st.session_state.setdefault("f_tag", [])
    # re-assign so widget state survives page switches
    for k in ["f_date", "f_tag", *opts]:
        st.session_state[k] = st.session_state[k]

    st.sidebar.title("💄 Filters")
    st.sidebar.date_input("Date range", min_value=dmin, max_value=dmax, key="f_date")
    st.sidebar.multiselect("Post Type", opts["f_type"], key="f_type")
    st.sidebar.multiselect("Campaign Type", opts["f_camp"], key="f_camp")
    st.sidebar.multiselect("Engagement Source", opts["f_src"], key="f_src")
    st.sidebar.multiselect("Audience Emotion", opts["f_emo"], key="f_emo")
    st.sidebar.multiselect("Hashtag (posts containing any)",
                           sorted(explode_hashtags(raw)["Hashtag"].unique()), key="f_tag")

    df = raw
    d = st.session_state["f_date"]
    if isinstance(d, tuple) and len(d) == 2:
        df = df[(df["Post Date"].dt.date >= d[0]) & (df["Post Date"].dt.date <= d[1])]
    df = df[df["Post Type"].isin(st.session_state["f_type"])
            & df["Campaign Type"].isin(st.session_state["f_camp"])
            & df["Engagement Source"].isin(st.session_state["f_src"])
            & df["Audience Emotion"].isin(st.session_state["f_emo"])]
    if st.session_state["f_tag"]:
        df = df[df["Hashtags"].str.contains("|".join(st.session_state["f_tag"]), regex=True, na=False)]
    st.sidebar.caption(f"Showing **{len(df):,}** of {len(raw):,} posts")
    if df.empty:
        st.warning("No posts match the current filters. Please widen your selection.")
        st.stop()
    return df
