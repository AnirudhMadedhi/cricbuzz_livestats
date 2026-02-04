import os
import sqlite3

db_path = os.environ.get("CRICKET_DB_PATH", "cricket.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# ----------------------------------
# Drop existing tables (safe reset)
# ----------------------------------
cur.executescript(
    """
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS player_format_stats;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS batting_stats;
DROP TABLE IF EXISTS bowling_stats;
"""
)

# ----------------------------------
# Core Tables (unchanged logic)
# ----------------------------------
cur.executescript(
    """
CREATE TABLE players (
    player_id TEXT PRIMARY KEY,
    full_name TEXT,
    country TEXT,
    playing_role TEXT,
    batting_style TEXT,
    bowling_style TEXT
);

CREATE TABLE teams (
    team_name TEXT PRIMARY KEY,
    country TEXT,
    wins INTEGER DEFAULT 0
);

CREATE TABLE venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT,
    city TEXT,
    country TEXT,
    capacity INTEGER
);

CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_description TEXT,
    team1 TEXT,
    team2 TEXT,
    winning_team TEXT,
    venue_id INTEGER,
    match_date TEXT,
    match_status TEXT,
    victory_margin INTEGER,
    victory_type TEXT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

CREATE TABLE player_format_stats (
    player_id TEXT,
    format TEXT CHECK(format IN ('test','odi','t20i')),
    high_score INTEGER,
    average REAL,
    strike_rate REAL,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
"""
)

# ----------------------------------
# New Tables for Q9–Q16
# ----------------------------------
cur.executescript(
    """
CREATE TABLE batting_stats (
    player_id TEXT,
    match_id INTEGER,
    format TEXT,
    innings INTEGER,
    batting_position INTEGER,
    runs INTEGER,
    balls INTEGER,
    strike_rate REAL,
    team TEXT,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE bowling_stats (
    player_id TEXT,
    match_id INTEGER,
    format TEXT,
    overs REAL,
    wickets INTEGER,
    economy_rate REAL,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);
"""
)

# ----------------------------------
# Seed Data
# ----------------------------------

# Players
cur.executemany(
    """
INSERT INTO players VALUES (?,?,?,?,?,?)
""",
    [
        ("virat_kohli", "Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium"),
        ("bumrah", "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("stokes", "Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
        ("jadeja", "Ravindra Jadeja", "India", "All-rounder", "Left-hand bat", "Left-arm spin"),
    ],
)

# Teams
cur.executemany(
    """
INSERT INTO teams VALUES (?,?,?)
""",
    [
        ("India", "India", 500),
        ("Australia", "Australia", 480),
        ("England", "England", 430),
    ],
)

# Venues
cur.executemany(
    """
INSERT INTO venues (venue_name, city, country, capacity)
VALUES (?,?,?,?)
""",
    [
        ("Wankhede Stadium", "Mumbai", "India", 33000),
        ("The Oval", "London", "England", 25500),
    ],
)

# Matches
cur.executemany(
    """
INSERT INTO matches
(match_description, team1, team2, winning_team, venue_id, match_date,
 match_status, victory_margin, victory_type)
VALUES (?,?,?,?,?,?,?,?,?)
""",
    [
        ("IND vs AUS 1st ODI", "India", "Australia", "India", 1, "2024-11-24", "Completed", 45, "Runs"),
        ("ENG vs IND Test Match", "England", "India", "England", 2, "2025-02-02", "Completed", 4, "Wickets"),
    ],
)

# Player format stats (career level)
cur.executemany(
    """
INSERT INTO player_format_stats VALUES (?,?,?,?,?)
""",
    [
        ("virat_kohli", "odi", 183, 58.0, 92.5),
        ("virat_kohli", "t20i", 94, 52.7, 137.6),
        ("stokes", "test", 258, 36.0, 58.4),
        ("jadeja", "odi", 87, 34.5, 84.2),
    ],
)

# Batting stats (match level)
cur.executemany(
    """
INSERT INTO batting_stats
(player_id, match_id, format, innings, batting_position, runs, balls, strike_rate, team)
VALUES (?,?,?,?,?,?,?,?,?)
""",
    [
        ("virat_kohli", 1, "odi", 1, 3, 112, 119, 94.1, "India"),
        ("stokes", 2, "test", 1, 5, 89, 140, 63.5, "England"),
        ("jadeja", 1, "odi", 1, 6, 45, 50, 90.0, "India"),
    ],
)


# Bowling stats (match level)
cur.executemany(
    """
INSERT INTO bowling_stats VALUES (?,?,?,?,?,?)
""",
    [
        ("bumrah", 1, "odi", 9.0, 4, 4.2),
        ("jadeja", 1, "odi", 10.0, 2, 3.8),
        ("stokes", 2, "test", 18.0, 3, 2.9),
    ],
)

conn.commit()
conn.close()

print(f"✅ Database created and fully seeded at: {db_path}")
