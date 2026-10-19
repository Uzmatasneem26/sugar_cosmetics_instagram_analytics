import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils import setup, get_filtered, fmt, style, explode_hashtags, BRAND, PALETTE

setup("Recommendations", "🎯")
df = get_filtered()
st.title("🎯 Strategic Recommendations")
st.caption("Generated from the filtered data. Differences between categories are small in this dataset, "
           "so treat them as tests to run, not proof.")

def best(col):
    s = df.groupby(col, observed=True)["Engagement Rate"].mean().sort_values(ascending=False)
    return s.index[0], s.iloc[0], s.index[-1], s.iloc[-1]

bt, bt_v, wt, wt_v = best("Post Type")
bd, bd_v, wd, wd_v = best("Weekday")
bc, bc_v, wc, wc_v = best("Campaign Type")
be, be_v, we, we_v = best("Audience Emotion")
bs, bs_v, ws, ws_v = best("Engagement Source")
mh = explode_hashtags(df).groupby("Hashtag").agg(U=("Post ID", "count"), ER=("Engagement Rate", "mean"))
ppm = df.groupby("Month")["Post ID"].count()
share = df["Shares"].sum() / df["Reach"].sum() * 100
save = df["Saves"].sum() / df["Reach"].sum() * 100
conv = df["Follows"].sum() / df["Profile Visits"].sum() * 100

st.header("Key takeaways")
st.markdown(f"""
- **Best format:** **{bt}** ({bt_v:.2f}% engagement); **{wt}** trails ({wt_v:.2f}%).
- **Best day:** **{bd}** ({bd_v:.2f}%); weakest is **{wd}** ({wd_v:.2f}%).
- **Best campaign:** **{bc}** ({bc_v:.2f}%) vs **{wc}** ({wc_v:.2f}%).
- **Best audience emotion:** **{be}** ({be_v:.2f}%); lowest is **{we}**.
- **Best source:** **{bs}** ({bs_v:.2f}%) vs **{ws}** ({ws_v:.2f}%).
- **Top hashtag:** **{mh['ER'].idxmax()}** ({mh['ER'].max():.2f}% avg engagement).
- Average engagement is **{df['Engagement Rate'].mean():.2f}%**; **{conv:.1f}%** of profile visits become follows.
""")
st.header("Recommended posting strategy")
st.markdown(f"""
- **Content mix:** weight more toward **{bt}**; keep **{wt}** for variety.
- **Timing:** put priority launches on **{bd}**, lighter content on **{wd}**.
- **Frequency:** monthly volume ranges {int(ppm.min()):,} to {int(ppm.max()):,} posts; keep it steady.
- **Campaigns:** scale **{bc}**; test sharper hooks for **{wc}**.
- **Tone:** lean into **{be}**-driven creative.
""")
st.header("Improving engagement and follower growth")
st.markdown(f"""
- Shares ({share:.2f}% of reach) and saves ({save:.2f}%) are low: add save-worthy tutorials and shade guides, plus share prompts.
- Lift the profile-visit to follow step ({conv:.1f}%) with a clear bio, highlights and a pinned best post.
- Invest in **{bs}** activity and review the weakest source (**{ws}**).
""")
st.header("Gaps and campaign ideas")
st.markdown(f"""
- **Gap:** **{wt}** and **{wc}** underperform; A/B test hooks and timing before cutting them.
- **Gap:** no hour-of-day or caption data, so timing and messaging themes can't be analysed yet.
- **Idea:** a recurring **{bc}** series on **{bd}**s in **{bt}** format with a branded hashtag.
- **Idea:** creator collabs around launches, then UGC reposts to raise shares and follows.
- **Idea:** "Save this for later" shade-match carousels to lift saves.
""")
st.download_button("Download filtered data (CSV)", df.drop(columns=["Post Label"]).to_csv(index=False),
                   file_name="sugar_cosmetics_filtered.csv", mime="text/csv")
