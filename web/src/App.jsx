import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const HEROES = ["elephant", "owl", "turtle", "bunny"];
const PLACES = ["forest", "seaside", "starry_sky"];
const MINUTES = [5, 10, 15];

export default function App() {
  const [ageBand, setAgeBand] = useState("5-6");
  const [hero, setHero] = useState("owl");
  const [place, setPlace] = useState("forest");
  const [minutes, setMinutes] = useState(5);

  const [loading, setLoading] = useState(false);
  const [story, setStory] = useState(null);
  const [error, setError] = useState("");

  async function makeStory() {
    setLoading(true);
    setError("");
    setStory(null);
    try {
      const res = await fetch(`${API}/stories`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ age_band: ageBand, hero, place, minutes }),
      });
      if (!res.ok) throw new Error(`The server said ${res.status}`);
      setStory(await res.json());
    } catch (e) {
      setError(`Could not make a story: ${e.message}. Is the API running?`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <h1>Sleepy Time Stories</h1>
      <p className="sub">Pick a hero and a place. A calm story will be ready in a few minutes.</p>

      <label>Age
        <select value={ageBand} onChange={(e) => setAgeBand(e.target.value)}>
          <option>3-4</option><option>5-6</option><option>7-8</option>
        </select>
      </label>

      <div className="group">
        <span>Hero</span>
        {HEROES.map((h) => (
          <button key={h} className={h === hero ? "chip on" : "chip"} onClick={() => setHero(h)}>{h}</button>
        ))}
      </div>

      <div className="group">
        <span>Place</span>
        {PLACES.map((p) => (
          <button key={p} className={p === place ? "chip on" : "chip"} onClick={() => setPlace(p)}>
            {p.replace("_", " ")}
          </button>
        ))}
      </div>

      <div className="group">
        <span>Length</span>
        {MINUTES.map((m) => (
          <button key={m} className={m === minutes ? "chip on" : "chip"} onClick={() => setMinutes(m)}>{m} min</button>
        ))}
      </div>

      <button className="start" onClick={makeStory} disabled={loading}>
        {loading ? "Writing and checking your story…" : "Make my story"}
      </button>

      {error && <p className="error">{error}</p>}

      {story && (
        <section className="player">
          <h2>{story.title}</h2>
          <p className="meta">
            {story.status === "approved" ? "Checked and approved" : "A favourite safe story"} ·{" "}
            {story.attempts} attempt(s) · {story.music} music
          </p>
          <audio controls autoPlay src={`${API}${story.audio_url}`} />
        </section>
      )}
    </main>
  );
}