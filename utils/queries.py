# Store ready-to-run sample queries aligned with the PDF prompt.
QUERIES = {
    "Q1 - India players basic":
        "SELECT full_name, playing_role, batting_style, bowling_style FROM players WHERE country='India' ORDER BY full_name;",
    "Q2 - Matches in last 30 days":
        "SELECT match_description, team1, team2, venue_name, venue_city, match_date FROM matches WHERE match_date >= date('now','-30 day') ORDER BY match_date DESC;",
    "Q5 - Team wins (sample)":
        "SELECT team_name, wins FROM teams ORDER BY wins DESC;",
    "Q7 - Format max score (sample)":
        "SELECT format, MAX(high_score) AS top_score FROM player_format_stats GROUP BY format ORDER BY top_score DESC;",
}
