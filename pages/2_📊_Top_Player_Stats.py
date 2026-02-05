import streamlit as st
import pandas as pd

from utils.api_handler import get_top_batters, get_top_bowlers, get_top_stats

st.set_page_config(page_title="Top Player Stats", layout="wide")

st.title("📊 Top Player Stats")

# ---------------------------
# Format Selection
# ---------------------------
fmt = st.selectbox(
    "Format",
    options=["odi", "test", "t20"],
    index=0
)

# ---------------------------
# Top Batters
# ---------------------------
st.subheader("🏏 Top Batters (ICC Rankings)")

batters_res = get_top_batters(fmt)

if not batters_res["ok"]:
    st.error(f"Batters API Error: {batters_res['error']}")
else:
    data = batters_res["data"].get("rank", [])

    if not data:
        st.warning("No batting data available.")
    else:
        df = pd.DataFrame(data)
        cols = ["rank", "name", "country", "rating"]
        df = df[[c for c in cols if c in df.columns]]
        st.dataframe(df, use_container_width=True)

# ---------------------------
# Top Bowlers
# ---------------------------
st.subheader("🎯 Top Bowlers (ICC Rankings)")

bowlers_res = get_top_bowlers(fmt)

if not bowlers_res["ok"]:
    st.error(f"Bowlers API Error: {bowlers_res['error']}")
else:
    data = bowlers_res["data"].get("rank", [])

    if not data:
        st.warning("No bowling data available.")
    else:
        df = pd.DataFrame(data)
        cols = ["rank", "name", "country", "rating"]
        df = df[[c for c in cols if c in df.columns]]
        st.dataframe(df, use_container_width=True)

# ==================================================
# SECTION 3: HISTORICAL TOP STATS (CRICBUZZ)
# ==================================================
st.subheader("📈 Historical Top Stats (Cricbuzz)")

fmt_map = {
    "Test": 0,
    "ODI": 1,
    "T20": 2
}

col1, col2 = st.columns(2)

with col1:
    record_format = st.selectbox(
        "Format",
        options=list(fmt_map.keys()),
        key="topstats_fmt"
    )

with col2:
    record_type = st.selectbox(
        "Stat Type",
        options=[
            ("Most Runs", "mostRuns"),
            ("Most Wickets", "mostWickets"),
            ("Highest Score", "highestScore"),
            ("Best Average", "bestAverage"),
        ],
        format_func=lambda x: x[0],
        key="topstats_type"
    )

stats_res = get_top_stats(
    stats_type=record_type[1],
    format_id=fmt_map[record_format]
)

if not stats_res["ok"]:
    st.error(f"Top Stats API Error: {stats_res['error']}")
else:
    headers = stats_res["data"].get("headers", [])
    values = stats_res["data"].get("values", [])

    if not headers or not values:
        st.warning("No data available.")
    else:
        # --- FIX: Cricbuzz returns an extra leading value ---
        clean_rows = []
        for v in values:
            row = v.get("values", [])
            if len(row) > len(headers):
                row = row[-len(headers):]  # drop extra index
            clean_rows.append(row)

        df = pd.DataFrame(clean_rows, columns=headers)

        st.dataframe(df, use_container_width=True)
