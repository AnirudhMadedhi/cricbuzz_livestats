import os
import time
import requests
from typing import Any, Dict, Optional, List

def _rapid_headers() -> Dict[str, str]:
    # Prefer Streamlit secrets if available
    api_key = os.environ.get("RAPIDAPI_KEY")
    host = os.environ.get("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
    return {
        "x-rapidapi-key": api_key or "",
        "x-rapidapi-host": host,
    }

def _get_base_url() -> str:
    return os.environ.get("CRICBUZZ_BASE_URL", "https://cricbuzz-cricket.p.rapidapi.com")

def safe_get(path: str, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> Dict[str, Any]:
    """HTTP GET wrapper with basic error handling. Returns a dict with keys: ok, status, data, error."""
    url = f"{_get_base_url()}{path}"
    headers = _rapid_headers()
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        if resp.status_code == 200:
            try:
                return {"ok": True, "status": 200, "data": resp.json(), "error": None}
            except Exception as je:
                return {"ok": False, "status": 200, "data": None, "error": f"JSON parse error: {je}"}
        return {"ok": False, "status": resp.status_code, "data": None, "error": resp.text[:400]}
    except Exception as e:
        return {"ok": False, "status": 0, "data": None, "error": str(e)}

# --- Cricbuzz convenience endpoints (RapidAPI) ---
def get_live_matches():
    return safe_get("/matches/v1/live")

def get_recent_matches():
    return safe_get("/matches/v1/recent")

# def get_top_batters(format_type: str = "odi"): #End Point for retriving data of top batsman as per the format(Test,ODI,T20) selected
#     # returns ICC batting rankings instead
#     return safe_get(f"/stats/v1/icc/rankings/{format_type}/batsmen") 

# def get_top_bowlers(format_type: str = "odi"):
#     # returns ICC bowling rankings instead
#     return safe_get(f"/stats/v1/icc/rankings/{format_type}/bowlers")

# def get_top_batters():
#     return safe_get("/stats/v1/icc/rankings/batsmen")

# def get_top_bowlers():
#     return safe_get("/stats/v1/icc/rankings/bowlers")
# def get_top_batters():
#     return safe_get("/stats/v1/rankings/batsmen")

# def get_top_bowlers():
#     return safe_get("/stats/v1/rankings/bowlers")

def get_top_batters(format_type: str):
    return safe_get(
        "/stats/v1/rankings/batsmen",
        params={"formatType": format_type}
    )

def get_top_bowlers(format_type: str):
    return safe_get(
        "/stats/v1/rankings/bowlers",
        params={"formatType": format_type}
    )




def search_player(name: str):
    return safe_get("/stats/v1/player/search", params={"plrN": name})

def player_summary(player_id: int):
    return safe_get(f"/stats/v1/player/{player_id}")
