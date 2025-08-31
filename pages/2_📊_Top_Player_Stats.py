import streamlit as st
from utils.api_handler import get_top_batters, get_top_bowlers

st.title("📊 Top Player Stats")

fmt = st.selectbox("Format", ["odi", "test", "t20i"], index=0)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Batters (Most Runs)")
    res = get_top_batters(fmt)
    if res["ok"]:
        st.json(res["data"])
    else:
        st.error(f"Error: {res['status']} - {res['error']}")

with col2:
    st.subheader("Top Bowlers (Most Wickets)")
    res2 = get_top_bowlers(fmt)
    if res2["ok"]:
        st.json(res2["data"])
    else:
        st.error(f"Error: {res2['status']} - {res2['error']}")
