
export type Sport = 'NBA' | 'NFL' | 'MLB' | 'NHL'

export interface SportsbookOdds {
  sportsbook: string
  away: number
  home: number
}

export interface Game {
  id: string
  sport: Sport
  away: string
  home: string
  odds: SportsbookOdds[]
}

const API_BASE_URL = 'http://127.0.0.1:8000'

export async function fetchGames(): Promise<Game[]> {
  const response = await fetch(`${API_BASE_URL}/api/games`)

  if (!response.ok) {
    throw new Error(`Failed to fetch games: ${response.status}`)
  }

  return response.json()
}
