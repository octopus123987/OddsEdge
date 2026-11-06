
import { useEffect, useState } from 'react'
import { fetchGames, type Game, type Sport } from './services/api'
import './App.css'

const SPORTS: Sport[] = ['NBA', 'NFL', 'MLB', 'NHL']

function App() {
  const [selectedSport, setSelectedSport] = useState<Sport>('NBA')
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadGames() {
      try {
        const data = await fetchGames()
        setGames(data)
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : 'Something went wrong'
        )
      } finally {
        setLoading(false)
      }
    }

    loadGames()
  }, [])

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
        {SPORTS.map((sport) => (
          <button
            key={sport}
            className={selectedSport === sport ? 'active' : ''}
            onClick={() => setSelectedSport(sport)}
          >
            {sport}
          </button>
        ))}
      </nav>

      <main>
        <h2>{selectedSport} Odds Comparison</h2>
        <p className="demo-label">
          Demonstration data — not live odds
        </p>

        {loading && <p>Loading games...</p>}

        {error && (
          <p role="alert" style={{ color: '#f87171' }}>
            Error: {error}
          </p>
        )}

        {!loading && !error && filteredGames.length === 0 && (
          <p>No games available for this sport yet.</p>
        )}

        {!loading && !error && filteredGames.map((game) => {
          const bestAway = Math.max(
            ...game.odds.map((o) => o.away)
          )
          const bestHome = Math.max(
            ...game.odds.map((o) => o.home)
          )

          return (
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
                  {game.odds.map((book) => (
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
                  ))}
                </tbody>
              </table>
            </section>
          )
        })}
      </main>
    </div>
  )
}

export default App
