import os
import sqlite3

db_path = os.environ.get("CRICKET_DB_PATH", "cricket.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Drop & create basic tables
cur.executescript(
    '''
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS player_format_stats;

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
    wins INTEGER DEFAULT 0
);

CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_description TEXT,
    team1 TEXT,
    team2 TEXT,
    venue_name TEXT,
    venue_city TEXT,
    match_date TEXT
);

CREATE TABLE player_format_stats (
    player_id TEXT,
    format TEXT CHECK(format IN ('test','odi','t20i')),
    high_score INTEGER,
    avg REAL,
    sr REAL
);
'''
)

# Seed a few rows
cur.executemany(
    "INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style) VALUES (?,?,?,?,?,?)",
    [
        ("virat_kohli", "Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium"),
        ("bumrah", "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("stokes", "Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
    ],
)
cur.executemany(
    "INSERT INTO teams (team_name, wins) VALUES (?,?)",
    [
        ("India", 500),
        ("Australia", 480),
        ("England", 430),
    ],
)
cur.executemany(
    "INSERT INTO matches (match_description, team1, team2, venue_name, venue_city, match_date) VALUES (?,?,?,?,?,?)",
    [
        ("IND vs AUS 1st ODI", "India", "Australia", "Wankhede", "Mumbai", "2024-11-24"),
        ("ENG vs SA 2nd Test", "England", "South Africa", "The Oval", "London", "2025-02-02"),
    ],
)
cur.executemany(
    "INSERT INTO player_format_stats (player_id, format, high_score, avg, sr) VALUES (?,?,?,?,?)",
    [
        ("virat_kohli", "odi", 183, 58.0, 92.5),
        ("virat_kohli", "t20i", 94, 52.7, 137.6),
        ("stokes", "test", 258, 36.0, 58.4),
    ],
)

conn.commit()
conn.close()
print(f"Database created and seeded at: {db_path}")
