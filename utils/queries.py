"""
Centralized SQL queries for Cricbuzz LiveStats – SQL Analytics Page
Beginner Level: Questions 1–8
"""

QUERIES = {

    "Q1": {
        "title": "Players representing India",
        "level": "Beginner",
        "query": """
            SELECT
                full_name,
                playing_role,
                batting_style,
                bowling_style
            FROM players
            WHERE country = 'India'
            ORDER BY full_name;
        """
    },

    "Q2": {
        "title": "Matches played in the last 30 days",
        "level": "Beginner",
        "query": """
            SELECT
                match_description,
                team1,
                team2,
                venue_name,
                venue_city,
                match_date
            FROM matches
            WHERE match_date >= DATE('now', '-30 day')
            ORDER BY match_date DESC;
        """
    },

    "Q3": {
        "title": "Top 10 highest run scorers in ODI cricket",
        "level": "Beginner",
        "query": """
            SELECT
                p.full_name AS player_name,
                SUM(b.runs) AS total_runs,
                ROUND(AVG(b.average), 2) AS batting_average,
                SUM(b.centuries) AS centuries
            FROM batting_stats b
            JOIN players p ON b.player_id = p.player_id
            WHERE b.format = 'ODI'
            GROUP BY p.player_id
            ORDER BY total_runs DESC
            LIMIT 10;
        """
    },

    "Q4": {
        "title": "Cricket venues with seating capacity over 25,000",
        "level": "Beginner",
        "query": """
            SELECT
                venue_name,
                city,
                country,
                capacity
            FROM venues
            WHERE capacity > 25000
            ORDER BY capacity DESC;
        """
    },

    "Q5": {
        "title": "Total matches won by each team",
        "level": "Beginner",
        "query": """
            SELECT
                winning_team AS team_name,
                COUNT(*) AS total_wins
            FROM matches
            WHERE winning_team IS NOT NULL
            GROUP BY winning_team
            ORDER BY total_wins DESC;
        """
    },

    "Q6": {
        "title": "Count of players by playing role",
        "level": "Beginner",
        "query": """
            SELECT
                playing_role,
                COUNT(*) AS player_count
            FROM players
            GROUP BY playing_role
            ORDER BY player_count DESC;
        """
    },

    "Q7": {
        "title": "Highest individual batting score in each format",
        "level": "Beginner",
        "query": """
            SELECT
                format,
                MAX(high_score) AS highest_score
            FROM player_format_stats
            GROUP BY format
            ORDER BY highest_score DESC;
        """
    },

    "Q8": {
        "title": "Cricket series started in the year 2024",
        "level": "Beginner",
        "query": """
            SELECT
                series_name,
                host_country,
                match_type,
                start_date,
                total_matches
            FROM series
            WHERE strftime('%Y', start_date) = '2024'
            ORDER BY start_date;
        """
    },
  
    "Q9": { 
        "title": "All-rounders with 1000+ runs and 50+ wickets",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name AS player_name,
                SUM(b.runs) AS total_runs,
                SUM(w.wickets) AS total_wickets,
                b.format
            FROM players p
            JOIN batting_stats b ON p.player_id = b.player_id
            JOIN bowling_stats w 
                 ON p.player_id = w.player_id AND b.format = w.format
            WHERE p.playing_role = 'All-rounder'
            GROUP BY p.player_id, b.format
            HAVING total_runs > 1000 AND total_wickets > 50
            ORDER BY total_runs DESC;
        """
    },

    "Q10": {
        "title": "Last 20 completed matches",
        "level": "Intermediate",
        "query": """
            SELECT
                match_description,
                team1,
                team2,
                winning_team,
                victory_margin,
                victory_type,
                venue_name
            FROM matches
            WHERE match_status = 'Completed'
            ORDER BY match_date DESC
            LIMIT 20;
        """
    },

    "Q11": {
        "title": "Player performance across Test, ODI and T20 formats",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name AS player_name,
                SUM(CASE WHEN b.format = 'Test' THEN b.runs ELSE 0 END) AS test_runs,
                SUM(CASE WHEN b.format = 'ODI' THEN b.runs ELSE 0 END) AS odi_runs,
                SUM(CASE WHEN b.format = 'T20' THEN b.runs ELSE 0 END) AS t20_runs,
                ROUND(AVG(b.average), 2) AS overall_batting_average
            FROM players p
            JOIN batting_stats b ON p.player_id = b.player_id
            GROUP BY p.player_id
            HAVING COUNT(DISTINCT b.format) >= 2
            ORDER BY overall_batting_average DESC;
        """
    },

    "Q12": {
        "title": "Team performance at home vs away",
        "level": "Intermediate",
        "query": """
            SELECT
                m.winning_team AS team_name,
                CASE
                    WHEN v.country = t.country THEN 'Home'
                    ELSE 'Away'
                END AS match_location,
                COUNT(*) AS wins
            FROM matches m
            JOIN venues v ON m.venue_id = v.venue_id
            JOIN teams t ON m.winning_team = t.team_name
            WHERE m.winning_team IS NOT NULL
            GROUP BY team_name, match_location
            ORDER BY team_name, wins DESC;
        """
    },

    "Q13": {
        "title": "Batting partnerships of 100+ runs",
        "level": "Intermediate",
        "query": """
            SELECT
                p1.full_name AS batsman_1,
                p2.full_name AS batsman_2,
                (bs1.runs + bs2.runs) AS partnership_runs,
                bs1.innings
            FROM batting_stats bs1
            JOIN batting_stats bs2
                 ON bs1.match_id = bs2.match_id
                AND bs1.innings = bs2.innings
                AND bs1.batting_position + 1 = bs2.batting_position
            JOIN players p1 ON bs1.player_id = p1.player_id
            JOIN players p2 ON bs2.player_id = p2.player_id
            WHERE (bs1.runs + bs2.runs) >= 100
            ORDER BY partnership_runs DESC;
        """
    },

    "Q14": {
        "title": "Bowling performance at venues (min 3 matches)",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name AS bowler_name,
                v.venue_name,
                COUNT(DISTINCT m.match_id) AS matches_played,
                SUM(b.wickets) AS total_wickets,
                ROUND(AVG(b.economy_rate), 2) AS avg_economy
            FROM bowling_stats b
            JOIN players p ON b.player_id = p.player_id
            JOIN matches m ON b.match_id = m.match_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE b.overs >= 4
            GROUP BY p.player_id, v.venue_id
            HAVING matches_played >= 3
            ORDER BY total_wickets DESC;
        """
    },

    "Q15": {
        "title": "Player performance in close matches",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name AS player_name,
                COUNT(DISTINCT m.match_id) AS close_matches_played,
                ROUND(AVG(b.runs), 2) AS avg_runs,
                SUM(
                    CASE WHEN m.winning_team = b.team THEN 1 ELSE 0 END
                ) AS matches_won
            FROM batting_stats b
            JOIN matches m ON b.match_id = m.match_id
            JOIN players p ON b.player_id = p.player_id
            WHERE
                (m.victory_type = 'Runs' AND m.victory_margin < 50)
                OR
                (m.victory_type = 'Wickets' AND m.victory_margin < 5)
            GROUP BY p.player_id
            ORDER BY avg_runs DESC;
        """
    },

    "Q16": {
        "title": "Year-wise batting performance since 2020",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name AS player_name,
                strftime('%Y', m.match_date) AS year,
                COUNT(DISTINCT m.match_id) AS matches_played,
                ROUND(AVG(b.runs), 2) AS avg_runs,
                ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
            FROM batting_stats b
            JOIN matches m ON b.match_id = m.match_id
            JOIN players p ON b.player_id = p.player_id
            WHERE strftime('%Y', m.match_date) >= '2020'
            GROUP BY p.player_id, year
            HAVING matches_played >= 5
            ORDER BY player_name, year;
        """
    },

}
