
import os
import requests
from dotenv import load_dotenv

# Load our secret API key
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("ODDS_API_KEY")

# The Odds API endpoint for NBA games
url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

# Parameters sent to the API
params = {
    "apiKey": API_KEY,
    "regions": "us",
    "markets": "h2h",
    "oddsFormat": "american",
}

try:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    games = response.json()

    print("API request successful!")
    print(f"Number of NBA games found: {len(games)}")

    for game in games[:3]:
        print(f"\n{game['away_team']} vs {game['home_team']}")

        for bookmaker in game.get("bookmakers", [])[:3]:
            print(f"  Sportsbook: {bookmaker['title']}")

            for market in bookmaker.get("markets", []):
                for outcome in market.get("outcomes", []):
                    print(f"    {outcome['name']}: {outcome['price']}")

except requests.exceptions.RequestException as error:
    print(f"API request failed: {error}")
