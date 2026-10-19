# 💄 Instagram Performance Analytics: Sugar Cosmetics

An interactive, multipage **Streamlit** dashboard that analyses Sugar Cosmetics' Instagram performance and turns the findings into data-driven social media recommendations.

🔗 **Live app:** https://sugarcosmeticsinstagramanalytics-gfvr5ld3rvkaczysugc76f.streamlit.app/

---

## Problem Statement
Analyse Sugar Cosmetics' Instagram performance and design an interactive dashboard to recommend strategic social media decisions.

## Objectives
- Evaluate account performance based on engagement and reach
- Identify trends in content performance
- Find the best-performing content types, hashtags and posting days
- Analyse campaign, audience-emotion and follower-growth patterns
- Provide data-driven recommendations to refine the social media strategy

## Business Use Case: Instagram Performance Analytics for Sugar Cosmetics

* Identify high-performing content and posting days: Find which post types and weekdays get the most likes, comments, shares and saves.
* Understand engagement patterns over time: Track monthly and weekly trends to spot peaks, dips and posting consistency.
* Compare post formats (image, video, carousel): See which format gives the best engagement so content effort goes where it pays off.
* Maximize ROI from organic posts: Improve reach and engagement without paid promotion, using better timing, formats and hashtags.
* Recognize successful hashtags and campaigns: Find which hashtags and themes drive the most interaction, then reuse them.
* Evaluate account growth or stagnation: Check whether reach and engagement are rising, flat or falling, so problems are caught early.

## Dataset
`sugar_cosmetics_instagram_data.xlsx`: 50,000 posts (Apr 2024 to Apr 2025)

| Column | Description |
|---|---|
| Post Date | Date the post was published |
| Post Type | Image, Reel, Story or Video |
| Campaign Type | Campaign theme of the post (e.g., Tutorial, Giveaway) |
| Hashtags | Comma-separated hashtags used |
| Audience Emotion | Dominant audience emotion (e.g., Happy, Curious) |
| Engagement Source | Organic, Influencer, Collab, etc. |
| Impressions, Reach | Exposure metrics |
| Likes, Comments, Shares, Saves | Engagement metrics |
| Profile Visits, Follows | Growth metrics |

**Calculated fields**
- `Total Engagement` = Likes + Comments + Shares + Saves
- `Engagement Rate (%)` = Total Engagement / Reach × 100 (per post, then averaged)
- `Month`, `Weekday`, `Post Label` for trend and ranking views

## App Pages
| # | Page | What it shows |
|---|---|---|
| Home | `app.py` | Headline KPIs, page guide, data preview |
| 1 | KPI Overview | Total posts, likes, comments, reach, average engagement rate |
| 2 | Posting Trend | Posts and engagement rate per month |
| 3 | Top 10 Likes | Most-liked posts |
| 4 | Top 10 Engagement | Highest engagement-rate posts ("hidden gems") |
| 5 | Post Types | Image vs Reel vs Story vs Video comparison |
| 6 | Day of Week | Best days to post, weekday × post type heatmap |
| 7 | Engagement Funnel | Impressions → Reach → Likes → Comments → Shares → Saves |
| 8 | Hashtags | Usage, engagement rate and reach by hashtag |
| 9 | Campaign & Growth | Campaigns, emotions, sources, follow conversion, cumulative follows |
| 10 | Recommendations | Key takeaways, posting strategy, gaps and campaign ideas |

**Interactivity:** sidebar filters (date range, post type, campaign, engagement source, audience emotion, hashtag) apply to every page, and the recommendations update with them. Filtered data can be downloaded as CSV.

## Project Structure
```
sugar_multipage/
├── app.py                      # Home page
├── utils.py                    # Data loading, filters, styling
├── requirements.txt
├── sugar_cosmetics_instagram_data.xlsx
├── README.md
└── pages/
    ├── 1_KPI_Overview.py
    ├── 2_Posting_Trend.py
    ├── 3_Top_10_Likes.py
    ├── 4_Top_10_Engagement.py
    ├── 5_Post_Types.py
    ├── 6_Day_of_Week.py
    ├── 7_Engagement_Funnel.py
    ├── 8_Hashtags.py
    ├── 9_Campaign_and_Growth.py
    └── 10_Recommendations.py
```

## Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/sugar-cosmetics-instagram-analytics.git
cd sugar-cosmetics-instagram-analytics
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501.

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **Create app**, select the repo, branch `main`, main file `app.py`
4. Click **Deploy**

## Tech Stack
Python · Streamlit · Pandas · Plotly · OpenPyXL

## Notes & Limitations
- The dataset has no caption column, so top-10 posts are identified by ID, format, campaign and date.
- Differences between categories (post types, weekdays, hashtags) are small, with average engagement around 18.5% everywhere, so recommendations should be treated as hypotheses to A/B test.
- Only five distinct hashtags appear in the data, so hashtag rankings are close to flat.
- April 2024 and April 2025 are partial months, which makes them look lower in the trend chart.
- No hour-of-day data is available, so posting-time analysis is limited to weekday.

## Author
uzma_tasneem.R