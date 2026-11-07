
import os
import time

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Load the API key from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("ODDS_API_KEY")
ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

# Cache responses for 5 minutes to conserve API credits
CACHE_DURATION = 300
cached_games = []
last_fetch_time = 0

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


def fetch_live_games():
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ODDS_API_KEY is not configured",
        )

    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american",
    }

    try:
        response = requests.get(
            ODDS_API_URL,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        raw_games = response.json()

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve live sportsbook odds",
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
            "sport": "NBA",
            "away": away_team,
            "home": home_team,
            "odds": sportsbook_odds,
        })

    return games


@app.get("/api/games")
def get_games():
    global cached_games, last_fetch_time

    current_time = time.monotonic()

    if (
        last_fetch_time != 0
        and current_time - last_fetch_time < CACHE_DURATION
    ):
        return cached_games

    games = fetch_live_games()

    cached_games = games
    last_fetch_time = time.monotonic()

    return games
