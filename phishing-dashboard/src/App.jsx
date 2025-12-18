import { useState } from "react";
import { runAgent } from "./api";
import EmailCard from "./components/EmailCard";
import "./index.css";

export default function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const scanInbox = async () => {
    setLoading(true);
    setMessage("");
    try {
      const data = await runAgent();
      if (data.status === "idle") {
        setEmails([]);
        setMessage(data.message);
      } else {
        setEmails(data);
      }
    } catch {
      setMessage("Failed to connect to agent.");
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>
          <span className="icon">🛡️</span>
          Autonomous Phishing Agent
        </h1>
        <p className="subtitle">
          AI-powered inbox defense against phishing & social engineering
        </p>

        <button onClick={scanInbox} disabled={loading} className="scan-btn">
          {loading ? "Scanning…" : "Scan Inbox"}
        </button>

        {message && !loading && (
          <div className="empty-state">
            <p>{message}</p>
          </div>
        )}
      </header>

      <main className="email-grid">
        {emails.map((item, i) => (
          <EmailCard key={i} data={item} />
        ))}
      </main>
    </div>

  );
}