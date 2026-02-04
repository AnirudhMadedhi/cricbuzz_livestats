import streamlit as st
import pandas as pd
from utils.db_connection import get_connection
from utils.queries import QUERIES

st.title("🔍 SQL Analytics")
st.caption("Runs against the local SQLite DB (cricket.db by default).")

conn = get_connection()

# -------------------------------
# Query selector
# -------------------------------
query_keys = ["(custom)"] + list(QUERIES.keys())

selected_key = st.selectbox(
    "Preset queries",
    query_keys,
    format_func=lambda k: "Custom SQL"
    if k == "(custom)"
    else f"{k}: {QUERIES[k]['title']}",
)

# -------------------------------
# Metadata + SQL selection
# -------------------------------
if selected_key == "(custom)":
    sql_query = st.text_area(
        "SQL Query",
        placeholder="SELECT * FROM players LIMIT 10;",
        height=180,
    )
else:
    st.caption(f"Difficulty: {QUERIES[selected_key]['level']}")
    sql_query = st.text_area(
        "SQL Query",
        QUERIES[selected_key]["query"],
        height=180,
    )

# -------------------------------
# Run query
# -------------------------------
if st.button("Run Query", type="primary"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query.")
    else:
        try:
            df = pd.read_sql_query(sql_query, conn)
            st.dataframe(df, use_container_width=True)
            st.success(f"Returned {len(df)} rows.")
        except Exception as e:
            st.error(f"SQL Error: {e}")
