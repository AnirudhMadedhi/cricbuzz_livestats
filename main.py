import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics")

st.markdown(
    '''
Welcome! This dashboard provides:
- ⚡ **Live match updates** via the Cricbuzz API (RapidAPI)
- 📊 **Top player statistics**
- 🔍 **SQL-driven analytics** on a local database
- 🛠 **CRUD operations** to practice DB manipulation
Tip: Live endpoints are cached for 30–60 seconds to avoid hitting rate limits.
Developed by Anirudh Madedhi as a part of Guvi Data Science Project
'''
)

with st.sidebar:
    st.header("Navigation")
    st.page_link("main.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_🏏_Live_Matches.py", label="Live Matches", icon="🟢")
    st.page_link("pages/2_📊_Top_Player_Stats.py", label="Top Player Stats", icon="📈")
    st.page_link("pages/3_🔍_SQL_Analytics.py", label="SQL Analytics", icon="🧮")
    st.page_link("pages/4_🛠_CRUD_Operations.py", label="CRUD Operations", icon="🧰")
    st.page_link("pages/5_🧪_API_Tester.py", label="API Tester", icon="🔧")

st.info("Use the sidebar links to open the feature pages.", icon="➡️")
