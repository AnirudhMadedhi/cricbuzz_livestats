import streamlit as st
import pandas as pd
from utils.db_connection import db_cursor, get_connection

st.title("🛠 CRUD Operations")
st.caption("Manage sample Players & Teams tables in SQLite.")

tab1, tab2 = st.tabs(["Players", "Teams"])

# -------- Players --------
with tab1:
    st.subheader("Create / Update Player")
    with st.form("player_form", clear_on_submit=True):
        pid = st.text_input("Player ID (string)")
        name = st.text_input("Full Name")
        country = st.text_input("Country")
        role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        batting = st.text_input("Batting Style", value="Right-hand bat")
        bowling = st.text_input("Bowling Style", value="Right-arm medium")
        submitted = st.form_submit_button("Save Player")
        if submitted:
            with db_cursor() as cur:
                cur.execute(
                    "INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style) "
                    "VALUES (?,?,?,?,?,?) "
                    "ON CONFLICT(player_id) DO UPDATE SET full_name=excluded.full_name, country=excluded.country, "
                    "playing_role=excluded.playing_role, batting_style=excluded.batting_style, bowling_style=excluded.bowling_style;",
                    (pid, name, country, role, batting, bowling),
                )
            st.success(f"Saved player {name} ({pid}).")

    st.divider()
    st.subheader("Delete Player")
    del_id = st.text_input("Player ID to delete")
    if st.button("Delete", key="del_player"):
        with db_cursor() as cur:
            cur.execute("DELETE FROM players WHERE player_id=?", (del_id,))
        st.warning(f"Deleted player {del_id}.")

    st.divider()
    st.subheader("Players Table")
    df = pd.read_sql_query("SELECT * FROM players ORDER BY full_name;", get_connection())
    st.dataframe(df, use_container_width=True)

# -------- Teams --------
with tab2:
    st.subheader("Create / Update Team")
    with st.form("team_form", clear_on_submit=True):
        name = st.text_input("Team Name")
        wins = st.number_input("Wins", min_value=0, value=0)
        submitted2 = st.form_submit_button("Save Team")
        if submitted2:
            with db_cursor() as cur:
                cur.execute(
                    "INSERT INTO teams (team_name, wins) VALUES (?, ?) "
                    "ON CONFLICT(team_name) DO UPDATE SET wins=excluded.wins;",
                    (name, wins),
                )
            st.success(f"Saved team {name}.")

    st.divider()
    st.subheader("Delete Team")
    del_team = st.text_input("Team name to delete")
    if st.button("Delete", key="del_team"):
        with db_cursor() as cur:
            cur.execute("DELETE FROM teams WHERE team_name=?", (del_team,))
        st.warning(f"Deleted team {del_team}.")

    st.divider()
    st.subheader("Teams Table")
    df2 = pd.read_sql_query("SELECT * FROM teams ORDER BY wins DESC;", get_connection())
    st.dataframe(df2, use_container_width=True)
