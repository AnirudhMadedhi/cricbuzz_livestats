import os
import requests
import streamlit as st
from typing import Any, Dict, Optional


# -------------------------------
# Config helpers
# -------------------------------

def _get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Prefer Streamlit secrets, fallback to environment variables.
    """
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except Exception:
        return os.environ.get(key, default)


def _rapid_headers() -> Dict[str, str]:
    api_key = _get_secret("RAPIDAPI_KEY")
    host = _get_secret("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")

    if not api_key:
        raise RuntimeError("RAPIDAPI_KEY is missing. Check secrets.toml or env vars.")

    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host,
        "User-Agent": "Mozilla/5.0",        # 🔑 REQUIRED for Akamai
        "Accept": "application/json"
    }


def _get_base_url() -> str:
    return _get_secret(
        "CRICBUZZ_BASE_URL",
        "https://cricbuzz-cricket.p.rapidapi.com"
    )


# -------------------------------
# Core request wrapper
# -------------------------------

def safe_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 15
) -> Dict[str, Any]:
    """
    HTTP GET wrapper.
    Returns:
        {
            ok: bool,
            status: int,
            data: dict | None,
            error: str | None
        }
    """
    url = f"{_get_base_url()}{path}"

    try:
        response = requests.get(
            url,
            headers=_rapid_headers(),
            params=params,
            timeout=timeout
        )

        if response.status_code == 200:
            try:
                return {
                    "ok": True,
                    "status": 200,
                    "data": response.json(),
                    "error": None
                }
            except Exception as json_err:
                return {
                    "ok": False,
                    "status": 200,
                    "data": None,
                    "error": f"JSON parse error: {json_err}"
                }

        # Akamai / API error
        return {
            "ok": False,
            "status": response.status_code,
            "data": None,
            "error": response.text[:500]
        }

    except requests.exceptions.RequestException as req_err:
        return {
            "ok": False,
            "status": 0,
            "data": None,
            "error": str(req_err)
        }


# -------------------------------
# Cricbuzz convenience endpoints
# -------------------------------

def get_live_matches():
    return safe_get("/matches/v1/live")


def get_recent_matches():
    return safe_get("/matches/v1/recent")


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


def get_top_stats(stats_type: str = "mostRuns", format_id: int = 0):
    """
    format_id:
        0 = Test
        1 = ODI
        2 = T20
    stats_type:
        mostRuns, mostWickets, highestScore, bestAverage
    """
    return safe_get(
        f"/stats/v1/topstats/{format_id}",
        params={"statsType": stats_type}
    )


def search_player(name: str):
    return safe_get(
        "/stats/v1/player/search",
        params={"plrN": name}
    )


def player_summary(player_id: int):
    return safe_get(f"/stats/v1/player/{player_id}")
