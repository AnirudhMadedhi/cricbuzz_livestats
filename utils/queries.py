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
                m.match_description,
                m.team1,
                m.team2,
                v.venue_name,
                v.city AS venue_city,
                m.match_date
            FROM matches m
            JOIN venues v
                ON m.venue_id = v.venue_id
            WHERE m.match_date <= DATE('now', '-30 day')
            ORDER BY m.match_date DESC;

        """
    },

    "Q3": {
        "title": "Top 10 highest run scorers in ODI cricket",
        "level": "Beginner",
        "query": """
                    SELECT
                p.full_name AS player_name,
                pfs.runs AS total_runs,
                pfs.average AS batting_average,
                pfs.centuries AS centuries
            FROM player_format_stats pfs
            JOIN players p
                ON pfs.player_id = p.player_id
            WHERE pfs.format = 'odi'
            ORDER BY pfs.runs DESC
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
            SELECT *
            FROM series
            WHERE strftime('%Y', start_date) = '2024';

        """
    },
  
    "Q9": { 
        "title": "All-rounders with 1000+ runs and 50+ wickets",
        "level": "Intermediate",
        "query": """
           WITH batting AS (
                SELECT
                    player_id,
                    format,
                    SUM(runs) AS total_runs
                FROM batting_stats
                GROUP BY player_id, format
            ),
            bowling AS (
                SELECT
                    player_id,
                    format,
                    SUM(wickets) AS total_wickets
                FROM bowling_stats
                GROUP BY player_id, format
            )
            SELECT
                p.full_name AS player_name,
                b.total_runs,
                w.total_wickets,
                b.format
            FROM players p
            JOIN batting b ON p.player_id = b.player_id
            JOIN bowling w 
                ON b.player_id = w.player_id 
                AND b.format = w.format
            WHERE p.playing_role = 'Allrounder'
            AND b.total_runs > 1000
            AND w.total_wickets > 50
            ORDER BY b.total_runs DESC;

        """
    },

    "Q10": {
        "title": "Last 20 completed matches",
        "level": "Intermediate",
        "query": """
                    SELECT
                m.match_description,
                m.team1,
                m.team2,
                m.winning_team,
                m.victory_margin,
                m.victory_type,
                v.venue_name
            FROM matches m
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.match_status = 'Completed'
            ORDER BY m.match_date DESC
            LIMIT 20;

        """
    },

    "Q11": {
        "title": "Player performance across Test, ODI and T20 formats",
        "level": "Intermediate",
        "query": """
            SELECT
                p.full_name,
                SUM(CASE WHEN pfs.format = 'test' THEN pfs.runs ELSE 0 END) AS test_runs,
                SUM(CASE WHEN pfs.format = 'odi' THEN pfs.runs ELSE 0 END) AS odi_runs,
                SUM(CASE WHEN pfs.format = 't20i' THEN pfs.runs ELSE 0 END) AS t20i_runs,
                ROUND(AVG(pfs.average), 2) AS overall_avg
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            GROUP BY p.player_id
            HAVING COUNT(DISTINCT pfs.format) >= 2;

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
            AND bs1.team = bs2.team              -- ✅ SAME TEAM
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
    # =========================
# Advanced Level (Q17–Q25)
# =========================

    "Q17": {
        "title": "Impact of winning the toss on match outcomes",
        "level": "Advanced",
        "query": """
        SELECT
            md.toss_decision,
            COUNT(*) AS total_matches,
            SUM(CASE WHEN md.toss_winner = m.winning_team THEN 1 ELSE 0 END) AS toss_and_match_wins,
            ROUND(
                (SUM(CASE WHEN md.toss_winner = m.winning_team THEN 1 ELSE 0 END) * 100.0)
                / COUNT(*),
                2
            ) AS win_percentage
        FROM matches m
        JOIN match_details md ON m.match_id = md.match_id
        GROUP BY md.toss_decision;

        """
    },

    "Q18": {
        "title": "Most economical bowlers in limited-overs cricket",
        "level": "Advanced",
        "query": """
            SELECT
                p.full_name AS bowler_name,
                SUM(b.wickets) AS total_wickets,
                ROUND(SUM(b.overs * b.economy_rate) / SUM(b.overs), 2) AS economy_rate,
                COUNT(DISTINCT b.match_id) AS matches_played
            FROM bowling_stats b
            JOIN players p ON b.player_id = p.player_id
            WHERE b.format IN ('odi', 't20i')
            GROUP BY p.player_id
            HAVING matches_played >= 10
            ORDER BY economy_rate ASC;
        """
    },

    "Q19": {
        "title": "Most consistent batsmen since 2022",
        "level": "Advanced",
        "query": """
            WITH stats AS (
                SELECT
                    b.player_id,
                    b.runs,
                    AVG(b.runs) OVER (PARTITION BY b.player_id) AS avg_runs
                FROM batting_stats b
                JOIN matches m ON b.match_id = m.match_id
                WHERE strftime('%Y', m.match_date) >= '2022'
            )
            SELECT
                p.full_name AS player_name,
                ROUND(AVG(runs), 2) AS avg_runs,
                ROUND(AVG((runs - avg_runs)*(runs - avg_runs)), 2) AS variance
            FROM stats
            JOIN players p ON stats.player_id = p.player_id
            GROUP BY stats.player_id
            HAVING COUNT(*) >= 10
            ORDER BY variance ASC;
        """
    },

    "Q20": {
        "title": "Matches played and batting average by format",
        "level": "Advanced",
        "query": """
            SELECT
                p.full_name AS player_name,
                b.format,
                COUNT(DISTINCT b.match_id) AS matches_played,
                ROUND(AVG(b.runs), 2) AS batting_average
            FROM batting_stats b
            JOIN players p ON b.player_id = p.player_id
            GROUP BY p.player_id, b.format
            HAVING COUNT(DISTINCT b.match_id) >= 20
            ORDER BY player_name, b.format;
        """
    },

    "Q21": {
        "title": "Composite player performance ranking",
        "level": "Advanced",
        "query": """
            WITH batting AS (
                SELECT
                    player_id,
                    SUM(runs) * 0.01 +
                    AVG(strike_rate) * 0.3 AS batting_points
                FROM batting_stats
                GROUP BY player_id
            ),
            bowling AS (
                SELECT
                    player_id,
                    SUM(wickets) * 2 +
                    (6 - AVG(economy_rate)) * 2 AS bowling_points
                FROM bowling_stats
                GROUP BY player_id
            )
            SELECT
                p.full_name AS player_name,
                ROUND(
                    COALESCE(bat.batting_points, 0) +
                    COALESCE(bowl.bowling_points, 0),
                    2
                ) AS total_score
            FROM players p
            LEFT JOIN batting bat ON p.player_id = bat.player_id
            LEFT JOIN bowling bowl ON p.player_id = bowl.player_id
            ORDER BY total_score DESC;
        """
    },

    "Q22": {
        "title": "Head-to-head analysis between teams",
        "level": "Advanced",
        "query": """
            SELECT
                team1,
                team2,
                COUNT(*) AS matches_played,
                SUM(CASE WHEN winning_team = team1 THEN 1 ELSE 0 END) AS team1_wins,
                SUM(CASE WHEN winning_team = team2 THEN 1 ELSE 0 END) AS team2_wins
            FROM matches
            WHERE match_date >= DATE('now', '-3 years')
            GROUP BY team1, team2
            HAVING matches_played >= 5;
        """
    },

    "Q23": {
        "title": "Recent player form and momentum",
        "level": "Advanced",
        "query": """
            WITH recent AS (
                SELECT
                    b.player_id,
                    b.runs,
                    ROW_NUMBER() OVER (
                        PARTITION BY b.player_id
                        ORDER BY m.match_date DESC
                    ) AS rn
                FROM batting_stats b
                JOIN matches m ON b.match_id = m.match_id
            )
            SELECT
                p.full_name AS player_name,
                ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 2) AS avg_last_5,
                ROUND(AVG(CASE WHEN rn <= 10 THEN runs END), 2) AS avg_last_10
            FROM recent
            JOIN players p ON recent.player_id = p.player_id
            GROUP BY recent.player_id;
        """
    },

    "Q24": {
        "title": "Most successful batting partnerships",
        "level": "Advanced",
        "query": """
                    SELECT
                p1.full_name AS batsman_1,
                p2.full_name AS batsman_2,
                COUNT(*) AS partnerships,
                ROUND(AVG(bs1.runs + bs2.runs), 2) AS avg_runs
            FROM batting_stats bs1
            JOIN batting_stats bs2
                ON bs1.match_id = bs2.match_id
                AND bs1.innings = bs2.innings
                AND bs1.team = bs2.team              -- ✅ SAME TEAM CONSTRAINT
                AND bs1.batting_position + 1 = bs2.batting_position
            JOIN players p1 ON bs1.player_id = p1.player_id
            JOIN players p2 ON bs2.player_id = p2.player_id
            GROUP BY
                p1.full_name,
                p2.full_name
            HAVING partnerships >= 5
            ORDER BY avg_runs DESC;

        """
    },

    "Q25": {
        "title": "Quarterly player performance trend",
        "level": "Advanced",
        "query": """
            WITH quarterly AS (
                SELECT
                    b.player_id,
                    strftime('%Y-Q%m', m.match_date) AS period,
                    AVG(b.runs) AS avg_runs
                FROM batting_stats b
                JOIN matches m ON b.match_id = m.match_id
                GROUP BY b.player_id, period
            ),
            trends AS (
                SELECT
                    player_id,
                    period,
                    avg_runs,
                    avg_runs -
                    LAG(avg_runs) OVER (
                        PARTITION BY player_id
                        ORDER BY period
                    ) AS change
                FROM quarterly
            )
            SELECT
                p.full_name AS player_name,
                period,
                avg_runs,
                CASE
                    WHEN change > 0 THEN 'Improving'
                    WHEN change < 0 THEN 'Declining'
                    ELSE 'Stable'
                END AS trend
            FROM trends
            JOIN players p ON trends.player_id = p.player_id;
        """
    },


}
