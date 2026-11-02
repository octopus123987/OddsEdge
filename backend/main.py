from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


GAMES = [
    {
        "id": 1,
        "sport": "NBA",
        "away": "Boston Celtics",
        "home": "New York Knicks",
        "odds": [
            {"sportsbook": "DraftKings", "away": -110, "home": 100},
            {"sportsbook": "FanDuel", "away": -105, "home": -105},
            {"sportsbook": "BetMGM", "away": -115, "home": 105},
        ],
    },
    {
        "id": 2,
        "sport": "NFL",
        "away": "Buffalo Bills",
        "home": "Kansas City Chiefs",
        "odds": [
            {"sportsbook": "DraftKings", "away": 120, "home": -140},
            {"sportsbook": "FanDuel", "away": 125, "home": -145},
            {"sportsbook": "BetMGM", "away": 115, "home": -135},
        ],
    },
]


@app.get("/api/games")
def get_games():
    return GAMES
