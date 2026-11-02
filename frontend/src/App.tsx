
import { useState } from 'react'
import './App.css'

type Sport = 'NBA' | 'NFL' | 'MLB' | 'NHL'

type Game = {
  id: number
  sport: Sport
  away: string
  home: string
  odds: {
    sportsbook: string
    away: number
    home: number
  }[]
}

const games: Game[] = [
  {
    id: 1,
    sport: 'NBA',
    away: 'Boston Celtics',
    home: 'New York Knicks',
    odds: [
      { sportsbook: 'DraftKings', away: -110, home: +100 },
      { sportsbook: 'FanDuel', away: -105, home: -105 },
      { sportsbook: 'BetMGM', away: -115, home: +105 },
    ],
  },
  {
    id: 2,
    sport: 'NFL',
    away: 'Buffalo Bills',
    home: 'Kansas City Chiefs',
    odds: [
      { sportsbook: 'DraftKings', away: +120, home: -140 },
      { sportsbook: 'FanDuel', away: +125, home: -145 },
      { sportsbook: 'BetMGM', away: +115, home: -135 },
    ],
  },
]

function App() {
  const [selectedSport, setSelectedSport] =
    useState<Sport>('NBA')

  const filteredGames = games.filter(
    (game) => game.sport === selectedSport
  )

  return (
    <div className="dashboard">
      <header>
        <h1>OddsEdge</h1>
        <p>Sports Odds Comparison & Analytics</p>
      </header>

      <nav className="sports-nav">
        {(['NBA', 'NFL', 'MLB', 'NHL'] as Sport[]).map(
          (sport) => (
            <button
              key={sport}
              className={
                selectedSport === sport ? 'active' : ''
              }
              onClick={() => setSelectedSport(sport)}
            >
              {sport}
            </button>
          )
        )}
      </nav>

      <main>
        <h2>{selectedSport} Odds Comparison</h2>
        <p className="demo-label">
          Demonstration data — not live odds
        </p>

        {filteredGames.length === 0 && (
          <p>No games available for this sport yet.</p>
        )}

        {filteredGames.map((game) => (
          <section className="game-card" key={game.id}>
            <h3>{game.away} vs {game.home}</h3>

            <table>
              <thead>
                <tr>
                  <th>Sportsbook</th>
                  <th>{game.away}</th>
                  <th>{game.home}</th>
                </tr>
              </thead>

              <tbody>
                {game.odds.map((book) => {
                  const bestAway = Math.max(
                    ...game.odds.map((o) => o.away)
                  )

                  const bestHome = Math.max(
                    ...game.odds.map((o) => o.home)
                  )

                  return (
                    <tr key={book.sportsbook}>
                      <td>{book.sportsbook}</td>
                      <td className={
                        book.away === bestAway ? 'best' : ''
                      }>
                        {book.away > 0 ? '+' : ''}
                        {book.away}
                      </td>
                      <td className={
                        book.home === bestHome ? 'best' : ''
                      }>
                        {book.home > 0 ? '+' : ''}
                        {book.home}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </section>
        ))}
      </main>
    </div>
  )
}

export default App
