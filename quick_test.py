import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Encoding": "identity"
}

r = requests.get(
    url,
    headers=headers,
    timeout=15,
    proxies={"http": None, "https": None}
)

print(r.status_code)
print(r.text[:300])
