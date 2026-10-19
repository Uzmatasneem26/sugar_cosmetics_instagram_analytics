"""Home page. Run: streamlit run app.py"""
import streamlit as st
from utils import setup, get_filtered, fmt

setup("Home")
df = get_filtered()

st.title("💄 Instagram Performance Analytics: Sugar Cosmetics")
st.markdown("An interactive dashboard to evaluate Sugar Cosmetics' Instagram performance and "
            "support data-driven social media strategy. Use the **sidebar pages** to explore each analysis; "
            "the filters on the left apply to every page.")

c = st.columns(5)
c[0].metric("Posts", f"{len(df):,}")
c[1].metric("Total Reach", fmt(df["Reach"].sum()))
c[2].metric("Total Likes", fmt(df["Likes"].sum()))
c[3].metric("Avg Engagement Rate", f"{df['Engagement Rate'].mean():.2f}%")
c[4].metric("New Follows", fmt(df["Follows"].sum()))

st.subheader("Pages")
st.markdown("""
1. **KPI Overview**: headline account metrics
2. **Posting Trend**: posts per month
3. **Top 10 Likes**: most-liked posts
4. **Top 10 Engagement**: hidden gems by engagement rate
5. **Post Types**: Image vs Reel vs Story vs Video
6. **Day of Week**: best days to post
7. **Engagement Funnel**: Impressions → Reach → Likes → Comments → Shares → Saves
8. **Hashtags**: hashtag performance
9. **Campaign & Growth**: campaigns, emotions, sources, follower growth
10. **Recommendations**: strategy, gaps and campaign ideas
""")
st.subheader("Dataset preview")
st.dataframe(df.drop(columns=["Post Label"]).head(100), use_container_width=True, hide_index=True)
