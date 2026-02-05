import sqlite3
from datetime import date, timedelta
import random
from collections import defaultdict

# -------------------------------------------------
# FREEZE DATASET
# -------------------------------------------------
random.seed(42)

# -------------------------------------------------
# DB init (NEW DB ONLY)
# -------------------------------------------------
API_DB_PATH = "cricket_api.db"
conn = sqlite3.connect(API_DB_PATH)
cur = conn.cursor()

# -------------------------------------------------
# DROP TABLES
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
# CREATE TABLES (UNCHANGED)
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
    series_id INTEGER
);

CREATE TABLE match_details (
    match_id INTEGER PRIMARY KEY,
    format TEXT CHECK(format IN ('test','odi','t20i')),
    toss_winner TEXT,
    toss_decision TEXT CHECK(toss_decision IN ('bat','bowl')),
    batting_first_team TEXT
);

CREATE TABLE player_format_stats (
    player_id TEXT,
    format TEXT,
    runs INTEGER,
    centuries INTEGER,
    high_score INTEGER,
    average REAL,
    strike_rate REAL
);

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
# TEAMS
# -------------------------------------------------
teams = [
    "India", "Australia", "England",
    "South Africa", "Pakistan", "Sri Lanka"
]

cur.executemany(
    "INSERT INTO teams VALUES (?,?)",
    [(t, t) for t in teams]
)

# -------------------------------------------------
# PLAYERS (REAL, ACTIVE — 7 PER TEAM)
# -------------------------------------------------
players = [
    # India
    ("virat_kohli","Virat Kohli","India","Batsman","Right-hand bat","None"),
    ("rohit_sharma","Rohit Sharma","India","Batsman","Right-hand bat","Off-spin"),
    ("shubman_gill","Shubman Gill","India","Batsman","Right-hand bat","None"),
    ("bumrah","Jasprit Bumrah","India","Bowler","Right-hand bat","Right-arm fast"),
    ("shami","Mohammed Shami","India","Bowler","Right-hand bat","Right-arm fast"),
    ("siraj","Mohammed Siraj","India","Bowler","Right-hand bat","Right-arm fast"),
    ("jadeja","Ravindra Jadeja","India","All-rounder","Left-hand bat","Left-arm spin"),

    # Australia
    ("smith","Steve Smith","Australia","Batsman","Right-hand bat","Leg-spin"),
    ("warner","David Warner","Australia","Batsman","Left-hand bat","None"),
    ("labuschagne","Marnus Labuschagne","Australia","Batsman","Right-hand bat","Leg-spin"),
    ("cummins","Pat Cummins","Australia","Bowler","Right-hand bat","Right-arm fast"),
    ("starc","Mitchell Starc","Australia","Bowler","Left-hand bat","Left-arm fast"),
    ("hazlewood","Josh Hazlewood","Australia","Bowler","Right-hand bat","Right-arm fast"),
    ("maxwell","Glenn Maxwell","Australia","All-rounder","Right-hand bat","Off-spin"),

    # England
    ("root","Joe Root","England","Batsman","Right-hand bat","Off-spin"),
    ("bairstow","Jonny Bairstow","England","Batsman","Right-hand bat","None"),
    ("brook","Harry Brook","England","Batsman","Right-hand bat","None"),
    ("anderson","James Anderson","England","Bowler","Right-hand bat","Right-arm fast"),
    ("wood","Mark Wood","England","Bowler","Right-hand bat","Right-arm fast"),
    ("woakes","Chris Woakes","England","Bowler","Right-hand bat","Right-arm medium"),
    ("stokes","Ben Stokes","England","All-rounder","Left-hand bat","Right-arm fast"),

    # South Africa
    ("markram","Aiden Markram","South Africa","Batsman","Right-hand bat","Off-spin"),
    ("de_kock","Quinton de Kock","South Africa","Batsman","Left-hand bat","None"),
    ("van_der_dussen","Rassie van der Dussen","South Africa","Batsman","Right-hand bat","None"),
    ("rabada","Kagiso Rabada","South Africa","Bowler","Right-hand bat","Right-arm fast"),
    ("ngidi","Lungi Ngidi","South Africa","Bowler","Right-hand bat","Right-arm fast"),
    ("jansen","Marco Jansen","South Africa","Bowler","Left-hand bat","Left-arm fast"),
    ("maharaj","Keshav Maharaj","South Africa","All-rounder","Left-hand bat","Left-arm spin"),

    # Pakistan
    ("babar","Babar Azam","Pakistan","Batsman","Right-hand bat","None"),
    ("imam","Imam-ul-Haq","Pakistan","Batsman","Left-hand bat","None"),
    ("rizwan","Mohammad Rizwan","Pakistan","Batsman","Right-hand bat","None"),
    ("shaheen","Shaheen Afridi","Pakistan","Bowler","Left-hand bat","Left-arm fast"),
    ("naseem","Naseem Shah","Pakistan","Bowler","Right-hand bat","Right-arm fast"),
    ("haris","Haris Rauf","Pakistan","Bowler","Right-hand bat","Right-arm fast"),
    ("shadab","Shadab Khan","Pakistan","All-rounder","Right-hand bat","Leg-spin"),

    # Sri Lanka
    ("karunaratne","Dimuth Karunaratne","Sri Lanka","Batsman","Left-hand bat","None"),
    ("mendis","Kusal Mendis","Sri Lanka","Batsman","Right-hand bat","None"),
    ("nissanka","Pathum Nissanka","Sri Lanka","Batsman","Right-hand bat","None"),
    ("rajitha","Kasun Rajitha","Sri Lanka","Bowler","Right-hand bat","Right-arm fast"),
    ("chameera","Dushmantha Chameera","Sri Lanka","Bowler","Right-hand bat","Right-arm fast"),
    ("kumara","Lahiru Kumara","Sri Lanka","Bowler","Right-hand bat","Right-arm fast"),
    ("hasaranga","Wanindu Hasaranga","Sri Lanka","All-rounder","Right-hand bat","Leg-spin"),
]

cur.executemany("INSERT INTO players VALUES (?,?,?,?,?,?)", players)

# -------------------------------------------------
# VENUES
# -------------------------------------------------
venues = [
    ("Wankhede Stadium","Mumbai","India",33000),
    ("Lord's","London","England",30000),
    ("MCG","Melbourne","Australia",100000),
    ("Gaddafi Stadium","Lahore","Pakistan",27000),
    ("Newlands","Cape Town","South Africa",25000),
    ("R Premadasa Stadium","Colombo","Sri Lanka",35000),
]

cur.executemany(
    "INSERT INTO venues (venue_name,city,country,capacity) VALUES (?,?,?,?)",
    venues
)

# -------------------------------------------------
# SERIES (15+, 2022–2026, ≥3 in 2024)
# -------------------------------------------------
series = [
    ("India vs Australia Test Series","India","test","2022-02-01",4),
    ("England vs South Africa ODI Series","England","odi","2022-07-10",3),
    ("Pakistan vs Sri Lanka Test Series","Pakistan","test","2022-10-05",2),

    ("Ashes Series","England","test","2023-06-15",5),
    ("India vs England ODI Series","India","odi","2023-01-20",3),
    ("Australia vs Pakistan T20I Series","Australia","t20i","2023-11-10",3),

    ("ICC ODI World Cup","India","odi","2024-10-05",48),
    ("India vs South Africa Test Series","India","test","2024-02-01",3),
    ("England vs Sri Lanka T20I Series","England","t20i","2024-06-10",3),

    ("Australia vs India T20I Series","Australia","t20i","2025-01-15",5),
    ("Pakistan vs England ODI Series","Pakistan","odi","2025-03-20",3),
    ("South Africa vs Sri Lanka ODI Series","South Africa","odi","2025-09-01",3),

    ("India vs Pakistan ODI Series","India","odi","2026-02-10",3),
    ("Australia vs England Test Series","Australia","test","2026-06-01",5),
    ("Sri Lanka vs South Africa T20I Series","Sri Lanka","t20i","2026-11-05",3),
]

cur.executemany(
    "INSERT INTO series (series_name,host_country,match_type,start_date,total_matches) VALUES (?,?,?,?,?)",
    series
)

# -------------------------------------------------
# MATCHES + DETAILS
# -------------------------------------------------
start = date(2022,1,1)
series_ids = list(range(1, len(series)+1))

matches, details = [], []

for i in range(200):
    team1, team2 = random.sample(teams, 2)
    fmt = random.choice(["test","odi","t20i"])
    toss_winner = random.choice([team1, team2])
    toss_decision = random.choice(["bat","bowl"])
    batting_first = toss_winner if toss_decision=="bat" else team2 if toss_winner==team1 else team1

    matches.append((
        f"{team1} vs {team2} Match {i+1}",
        team1, team2,
        random.choice([team1, team2]),
        random.randint(1,len(venues)),
        (start + timedelta(days=i*5)).isoformat(),
        "Completed",
        random.randint(1,100),
        random.choice(["Runs","Wickets"]),
        random.choice(series_ids)
    ))

    details.append((i+1, fmt, toss_winner, toss_decision, batting_first))

cur.executemany("""
INSERT INTO matches
(match_description,team1,team2,winning_team,venue_id,
 match_date,match_status,victory_margin,victory_type,series_id)
VALUES (?,?,?,?,?,?,?,?,?,?)
""", matches)

cur.executemany("INSERT INTO match_details VALUES (?,?,?,?,?)", details)

# -------------------------------------------------
# PLAYER FORMAT STATS (ALL PLAYERS, ALL FORMATS)
# -------------------------------------------------
for pid, in cur.execute("SELECT player_id FROM players"):
    for fmt in ["test","odi","t20i"]:
        runs = random.randint(1000,14000)
        matches_played = random.randint(20,200)
        cur.execute(
            "INSERT INTO player_format_stats VALUES (?,?,?,?,?,?,?)",
            (
                pid, fmt,
                runs,
                runs // 100,
                random.randint(80,250),
                round(runs / matches_played, 2),
                round(random.uniform(60,150), 2),
            )
        )

# -------------------------------------------------
# MATCH-LEVEL STATS (ALL PLAYERS)
# -------------------------------------------------
team_players = defaultdict(list)
for pid, team in cur.execute("SELECT player_id, country FROM players"):
    team_players[team].append(pid)

batting_rows, bowling_rows, fielding_rows, partnership_rows = [], [], [], []

for mid, team1, team2, fmt in cur.execute("""
    SELECT m.match_id, m.team1, m.team2, d.format
    FROM matches m JOIN match_details d ON m.match_id = d.match_id
"""):
    for innings, team in enumerate([team1, team2], start=1):
        plist = team_players[team]
        random.shuffle(plist)

        for pos, pid in enumerate(plist, start=1):
            runs = random.randint(5,160)
            balls = random.randint(10,180)
            batting_rows.append(
                (pid, mid, fmt, innings, pos, runs, balls, round(runs/balls*100,1), team)
            )
            fielding_rows.append(
                (pid, mid, random.randint(0,2), random.randint(0,1), random.randint(0,1))
            )

        bowlers = [p for p in plist if p not in plist[:3]]
        for pid in bowlers:
            overs = random.uniform(4,10) if fmt!="test" else random.uniform(10,25)
            bowling_rows.append(
                (pid, mid, fmt, round(overs,1), random.randint(0,5), round(random.uniform(3,6),2))
            )

        for i in range(len(plist)-1):
            partnership_rows.append(
                (mid, innings, plist[i], plist[i+1], i+1, random.randint(30,250))
            )

cur.executemany("INSERT INTO batting_stats VALUES (?,?,?,?,?,?,?,?,?)", batting_rows)
cur.executemany("INSERT INTO bowling_stats VALUES (?,?,?,?,?,?)", bowling_rows)
cur.executemany("INSERT INTO fielding_stats VALUES (?,?,?,?,?)", fielding_rows)
cur.executemany("INSERT INTO partnerships VALUES (?,?,?,?,?,?)", partnership_rows)

conn.commit()
conn.close()

print("✅ cricket_api.db created EXACTLY as requested — real teams, real players, full data")
