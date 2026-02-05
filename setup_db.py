import os
import sqlite3
from datetime import date, timedelta
import random

# -------------------------------------------------
# FREEZE DATASET
# -------------------------------------------------
random.seed(42)

# -------------------------------------------------
# DB init
# -------------------------------------------------
db_path = os.environ.get("CRICKET_DB_PATH", "cricket.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# -------------------------------------------------
# Drop tables
# -------------------------------------------------
cur.executescript("""
DROP TABLE IF EXISTS partnerships;
DROP TABLE IF EXISTS fielding_stats;
DROP TABLE IF EXISTS bowling_stats;
DROP TABLE IF EXISTS batting_stats;
DROP TABLE IF EXISTS match_details;
DROP TABLE IF EXISTS player_format_stats;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS players;
""")

# -------------------------------------------------
# Core tables
# -------------------------------------------------
cur.executescript("""
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
    country TEXT
);

CREATE TABLE venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT,
    city TEXT,
    country TEXT,
    capacity INTEGER
);

CREATE TABLE series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name TEXT,
    host_country TEXT,
    match_type TEXT CHECK(match_type IN ('test','odi','t20i')),
    start_date TEXT,
    total_matches INTEGER
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
    series_id INTEGER,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (series_id) REFERENCES series(series_id)
);

CREATE TABLE match_details (
    match_id INTEGER PRIMARY KEY,
    format TEXT CHECK(format IN ('test','odi','t20i')),
    toss_winner TEXT,
    toss_decision TEXT CHECK(toss_decision IN ('bat','bowl')),
    batting_first_team TEXT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE player_format_stats (
    player_id TEXT,
    format TEXT,
    runs INTEGER,
    centuries INTEGER,
    high_score INTEGER,
    average REAL,
    strike_rate REAL,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
""")

# -------------------------------------------------
# Performance tables
# -------------------------------------------------
cur.executescript("""
CREATE TABLE batting_stats (
    player_id TEXT,
    match_id INTEGER,
    format TEXT,
    innings INTEGER,
    batting_position INTEGER,
    runs INTEGER,
    balls INTEGER,
    strike_rate REAL,
    team TEXT
);

CREATE TABLE bowling_stats (
    player_id TEXT,
    match_id INTEGER,
    format TEXT,
    overs REAL,
    wickets INTEGER,
    economy_rate REAL
);

CREATE TABLE fielding_stats (
    player_id TEXT,
    match_id INTEGER,
    catches INTEGER,
    stumpings INTEGER,
    run_outs INTEGER
);

CREATE TABLE partnerships (
    match_id INTEGER,
    innings INTEGER,
    player1_id TEXT,
    player2_id TEXT,
    batting_position_start INTEGER,
    partnership_runs INTEGER
);
""")

# -------------------------------------------------
# Seed master data
# -------------------------------------------------
players = [
    ("virat_kohli","Virat Kohli","India","Batsman","Right-hand bat","Right-arm medium"),
    ("rohit_sharma","Rohit Sharma","India","Batsman","Right-hand bat","Off-spin"),
    ("jadeja","Ravindra Jadeja","India","All-rounder","Left-hand bat","Left-arm spin"),
    ("bumrah","Jasprit Bumrah","India","Bowler","Right-hand bat","Right-arm fast"),
    ("stokes","Ben Stokes","England","All-rounder","Left-hand bat","Right-arm fast"),
    ("root","Joe Root","England","Batsman","Right-hand bat","Off-spin"),
    ("smith","Steve Smith","Australia","Batsman","Right-hand bat","Leg-spin"),
    ("warner","David Warner","Australia","Batsman","Left-hand bat","None"),
    ("starc","Mitchell Starc","Australia","Bowler","Left-hand bat","Left-arm fast"),
    ("buttler","Jos Buttler","England","Wicket-keeper","Right-hand bat","None"),
]

teams = [
    ("India","India"),
    ("England","England"),
    ("Australia","Australia")
]

venues = [
    ("Wankhede Stadium","Mumbai","India",33000),
    ("Eden Gardens","Kolkata","India",68000),
    ("Lord's","London","England",30000),
    ("MCG","Melbourne","Australia",100000),
    ("SCG","Sydney","Australia",48000)
]

cur.executemany("INSERT INTO players VALUES (?,?,?,?,?,?)", players)
cur.executemany("INSERT INTO teams VALUES (?,?)", teams)
cur.executemany(
    "INSERT INTO venues (venue_name,city,country,capacity) VALUES (?,?,?,?)",
    venues
)

# -------------------------------------------------
# Series data (Q8)
# -------------------------------------------------
cur.executemany(
    """
    INSERT INTO series
    (series_name, host_country, match_type, start_date, total_matches)
    VALUES (?,?,?,?,?)
    """,
    [
        ("India vs England ODI Series", "India", "odi", "2024-01-10", 3),
        ("Australia vs India T20I Series", "Australia", "t20i", "2024-11-05", 5),
        ("England vs Australia Test Series", "England", "test", "2023-07-01", 5),
    ],
)

# -------------------------------------------------
# Matches (2020–2026 spread)
# -------------------------------------------------
match_id = 1
matches = []
details = []

start = date(2020,1,5)
series_ids = [1, 2, 3]

for i in range(75):
    team1, team2 = random.sample(["India","England","Australia"], 2)
    winner = random.choice([team1, team2])
    venue_id = random.randint(1,5)
    fmt = random.choice(["odi","t20i","test"])
    margin = random.randint(1,45)
    vtype = random.choice(["Runs","Wickets"])
    toss_winner = random.choice([team1, team2])
    toss_decision = random.choice(["bat","bowl"])
    batting_first = toss_winner if toss_decision=="bat" else (team1 if toss_winner==team2 else team2)
    series_id = random.choice(series_ids)

    matches.append((
        f"{team1} vs {team2} Match {i+1}",
        team1, team2, winner,
        venue_id,
        (start + timedelta(days=i*25)).isoformat(),
        "Completed",
        margin,
        vtype,
        series_id
    ))

    details.append((match_id, fmt, toss_winner, toss_decision, batting_first))
    match_id += 1

cur.executemany("""
INSERT INTO matches
(match_description,team1,team2,winning_team,venue_id,match_date,
 match_status,victory_margin,victory_type,series_id)
VALUES (?,?,?,?,?,?,?,?,?,?)
""", matches)

cur.executemany("INSERT INTO match_details VALUES (?,?,?,?,?)", details)

# -------------------------------------------------
# Career stats
# -------------------------------------------------
format_stats = [
    ("virat_kohli","odi",13000,46,183,58.2,92.5),
    ("virat_kohli","t20i",4000,1,122,51.0,138.0),
    ("rohit_sharma","odi",12000,31,264,49.0,90.1),
    ("stokes","test",5800,11,258,37.0,56.0),
    ("jadeja","odi",2600,2,87,32.0,85.0),
    ("smith","test",9000,30,239,60.5,54.0)
]
cur.executemany("INSERT INTO player_format_stats VALUES (?,?,?,?,?,?,?)", format_stats)

# -------------------------------------------------
# Match-level stats (bulk)
# -------------------------------------------------
batting_rows = []
bowling_rows = []
fielding_rows = []
partnership_rows = []

for m in range(1, 76):
    fmt = details[m-1][1]
    innings = 1
    for idx, p in enumerate(players[:6]):
        runs = random.randint(10,130)
        balls = random.randint(15,140)
        batting_rows.append((
            p[0], m, fmt, innings, idx+1,
            runs, balls, round((runs/balls)*100,1), p[2]
        ))

    for p in players[3:9]:
        overs = random.uniform(4,10) if fmt!="test" else random.uniform(10,25)
        wickets = random.randint(0,4)
        bowling_rows.append((
            p[0], m, fmt,
            round(overs,1), wickets,
            round(random.uniform(3.0,6.5),2)
        ))

    for p in players[:6]:
        fielding_rows.append((p[0], m,
            random.randint(0,2),
            random.randint(0,1),
            random.randint(0,1)
        ))

    for i in range(1,5):
        partnership_rows.append((
            m, innings,
            players[i-1][0],
            players[i][0],
            i,
            random.randint(40,180)
        ))

cur.executemany("""
INSERT INTO batting_stats
(player_id,match_id,format,innings,batting_position,runs,balls,strike_rate,team)
VALUES (?,?,?,?,?,?,?,?,?)
""", batting_rows)

cur.executemany("INSERT INTO bowling_stats VALUES (?,?,?,?,?,?)", bowling_rows)
cur.executemany("INSERT INTO fielding_stats VALUES (?,?,?,?,?)", fielding_rows)
cur.executemany("INSERT INTO partnerships VALUES (?,?,?,?,?,?)", partnership_rows)

conn.commit()
conn.close()

print(f"✅ Database fully created, frozen, and seeded at: {db_path}")
