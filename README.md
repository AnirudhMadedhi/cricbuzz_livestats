# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A multi-page Streamlit app integrating Cricbuzz (via RapidAPI) and a local SQLite database for analytics + CRUD.

## 🚀 Quickstart
```bash
# 1) Create venv (optional) and install deps
pip install -r requirements.txt

# 2) Create DB with sample schema/data
python setup_db.py

# 3) Add your RapidAPI key
#   - Option A: set env var RAPIDAPI_KEY
#   - Option B: edit .streamlit/secrets.toml
# 4) Run
streamlit run main.py
```

## 🔑 Secrets / Env Vars
- `RAPIDAPI_KEY`: Your RapidAPI key for Cricbuzz
- `RAPIDAPI_HOST`: Default `cricbuzz-cricket.p.rapidapi.com`
- `CRICBUZZ_BASE_URL`: Default `https://cricbuzz-cricket.p.rapidapi.com`
- `CRICKET_DB_PATH`: SQLite file path (default `cricket.db`)

## 📂 Pages
- **Live Matches**: Live feed from `/matches/v1/live`
- **Top Player Stats**: Top batters/bowlers per format
- **SQL Analytics**: Run ad-hoc or preset queries on local DB
- **CRUD Operations**: Add/Update/Delete players & teams
- **API Tester**: Hit any Cricbuzz path with params

## 🗄 Sample Schema
We provide a small schema suitable for practice and the preset queries.

Tables:
- `players(player_id TEXT PRIMARY KEY, full_name TEXT, country TEXT, playing_role TEXT, batting_style TEXT, bowling_style TEXT)`
- `teams(team_name TEXT PRIMARY KEY, wins INTEGER)`
- `matches(id INTEGER PRIMARY KEY, match_description TEXT, team1 TEXT, team2 TEXT, venue_name TEXT, venue_city TEXT, match_date TEXT)`
- `player_format_stats(player_id TEXT, format TEXT, high_score INTEGER, avg REAL, sr REAL)

Run `python setup_db.py` to (re)create and seed the DB.

## ⚠️ Notes
- Cricbuzz RapidAPI may change paths/shape. The API Tester page helps you adapt quickly.
- Caching is used to lower rate-limit pressure.
- For production use, add retries/backoff and stricter input validation.
