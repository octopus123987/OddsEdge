import os
import time

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

# Load the API key from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("ODDS_API_KEY")
API_BASE_URL = "https://api.the-odds-api.com/v4/sports"

# Map our dashboard sports to The Odds API sport keys
SPORT_KEYS = {
    "NBA": "basketball_nba",
    "NFL": "americanfootball_nfl",
    "MLB": "baseball_mlb",
    "NHL": "icehockey_nhl",
}

# Cache each sport separately for 5 minutes
CACHE_DURATION = 300
games_cache = {}


app = FastAPI(title="OddsEdge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to OddsEdge API"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


def fetch_live_games(sport: str):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ODDS_API_KEY is not configured",
        )

    sport_key = SPORT_KEYS[sport]
    url = f"{API_BASE_URL}/{sport_key}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        raw_games = response.json()

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve {sport} odds",
        )

    games = []

    for raw_game in raw_games:
        away_team = raw_game["away_team"]
        home_team = raw_game["home_team"]
        sportsbook_odds = []

        for bookmaker in raw_game.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue

                outcomes = {
                    outcome["name"]: outcome["price"]
                    for outcome in market.get("outcomes", [])
                }

                if away_team in outcomes and home_team in outcomes:
                    sportsbook_odds.append({
                        "sportsbook": bookmaker["title"],
                        "away": outcomes[away_team],
                        "home": outcomes[home_team],
                    })

        games.append({
            "id": raw_game["id"],
            "sport": sport,
            "away": away_team,
            "home": home_team,
            "odds": sportsbook_odds,
        })

    return games


@app.get("/api/games")
def get_games(sport: str = Query(default="NBA")):
    sport = sport.upper()

    if sport not in SPORT_KEYS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported sport. Choose NBA, NFL, MLB, or NHL.",
        )

    current_time = time.monotonic()
    cached = games_cache.get(sport)

    if cached and current_time - cached["timestamp"] < CACHE_DURATION:
        return cached["games"]

    games = fetch_live_games(sport)

    games_cache[sport] = {
        "timestamp": time.monotonic(),
        "games": games,
    }

    return games
