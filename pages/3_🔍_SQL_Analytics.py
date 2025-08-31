import streamlit as st
import pandas as pd
from utils.db_connection import get_connection
from utils.queries import QUERIES

st.title("🔍 SQL Analytics")
st.caption("Runs against the local SQLite DB (cricket.db by default).")

conn = get_connection()

preset = st.selectbox("Preset queries", ["(custom)"] + list(QUERIES.keys()))
query = st.text_area("SQL Query", QUERIES.get(preset, ""), height=180, placeholder="SELECT * FROM players LIMIT 10;")

if st.button("Run Query", type="primary"):
    try:
        df = pd.read_sql_query(query, conn)
        st.dataframe(df, use_container_width=True)
        st.success(f"Returned {len(df)} rows.")
    except Exception as e:
        st.error(f"Error: {e}")
