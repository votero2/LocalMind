import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/task";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [events, setEvents] = useState([]);

  async function runTask(e) {
    setEvents([]);
    e.preventDefault();
    if (!question.trim() || loading) return;

    const task = question.trim();

    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: task }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const result = data.answer ?? "";

      setEvents(data.events ?? []);
      setAnswer(result);
      setHistory((previous) => [
        { question: task, answer: result },
        ...previous,
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>◈ LocalMind</h2>
        <p className="subtitle">Multi-Agent Orchestrator</p>

        <nav>
          <div className="nav-item active">▦ Dashboard</div>
          <div className="nav-item">◇ Agents</div>
          <div className="nav-item">◷ History</div>
        </nav>

        <div className="sidebar-footer">LocalMind v0.1</div>
      </aside>

      <main className="main">
        <header>
          <div>
            <h1>Agent Control Center</h1>
            <p>Manage tasks and monitor AI responses.</p>
          </div>
          <span className="status">● Local Environment</span>
        </header>

        <section className="stats">
          <div className="stat-card">
            <span>Tasks This Session</span>
            <strong>{history.length}</strong>
          </div>
          <div className="stat-card">
            <span>Configured Agent Modules</span>
            <strong>5</strong>
          </div>
          <div className="stat-card">
            <span>Execution</span>
            <strong>{loading ? "Running" : "Idle"}</strong>
          </div>
        </section>

        <div className="content-grid">
          <section className="panel">
            <h2>Agent Console</h2>
            <p>Send a request to your LocalMind agents.</p>

            <form onSubmit={runTask}>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask LocalMind to perform a task..."
                rows={6}
              />

              <button disabled={loading || !question.trim()}>
                {loading ? "Processing..." : "Run Task →"}
              </button>
            </form>
          </section>

          <section className="panel">
            <h2>AI Response</h2>
            <p>Latest response from the backend.</p>

            <div className="response">
              {error ? (
                <span className="error">{error}</span>
              ) : loading ? (
                "LocalMind is processing your request..."
              ) : answer ? (
                answer
              ) : (
                "No task executed yet."
              )}
            </div>
          </section>
        </div>

        <section className="panel agent-monitor">
          <h2>Agent Execution Monitor</h2>
          <p>Actual execution events from LocalMind.</p>

          {events.length === 0 ? (
            <div className="empty">No agent activity recorded yet.</div>
          ) : (
            <div className="event-list">
              {events.map((event, index) => (
                <div className="event-item" key={index}>
                  <div className="event-icon">
                    {event.status === "completed" ? "✓" : "◉"}
                  </div>

                  <div className="event-details">
                    <strong>{event.agent.replaceAll("_", " ")}</strong>
                    <p>{event.message}</p>
                  </div>

                  <span className={`event-status ${event.status}`}>
                    {event.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="panel history">
          <h2>Execution History</h2>
          <p>Tasks completed during this browser session.</p>

          {history.length === 0 ? (
            <div className="empty">No executions yet.</div>
          ) : (
            history.map((item, index) => (
              <div className="history-item" key={index}>
                <strong>{item.question}</strong>
                <p>{item.answer.slice(0, 180)}...</p>
              </div>
            ))
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
