import streamlit as st
import pandas as pd

from utils.api_handler import get_top_batters, get_top_bowlers

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
