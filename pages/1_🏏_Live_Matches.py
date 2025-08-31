import streamlit as st
from utils.api_handler import get_live_matches

st.title("🟢 Live Matches")

data = get_live_matches()

if not data.get("ok"):
    st.error(f"API error (status {data.get('status')}): {data.get('error')}")
else:
    payload = data.get("data", {})
    matches = payload.get("typeMatches", [])

    if not matches:
        st.info("There are no live matches at the moment.", icon="ℹ️")
    else:
        for group in matches:
            st.header(group.get("matchType", "Unknown Format").upper())

            for match in group.get("seriesMatches", []):
                series = match.get("seriesAdWrapper", {})
                series_name = series.get("seriesName", "Unknown Series")
                st.subheader(f"🏆 {series_name}")

                for m in series.get("matches", []):
                    info = m.get("matchInfo", {})
                    score = m.get("matchScore", {})

                    team1 = info.get("team1", {}).get("teamSName", "Team 1")
                    team2 = info.get("team2", {}).get("teamSName", "Team 2")
                    status = info.get("status", "Status Unknown")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"### {team1}")
                        if "team1Score" in score:
                            t1 = score["team1Score"]["inngs1"]
                            st.write(f"Runs: **{t1.get('runs','-')} / {t1.get('wickets','-')}**")
                            st.write(f"Overs: {t1.get('overs','-')}")

                    with col2:
                        st.markdown(f"### {team2}")
                        if "team2Score" in score:
                            t2 = score["team2Score"]["inngs1"]
                            st.write(f"Runs: **{t2.get('runs','-')} / {t2.get('wickets','-')}**")
                            st.write(f"Overs: {t2.get('overs','-')}")

                    st.markdown(f"**Match Status:** {status}")
                    st.markdown("---")
