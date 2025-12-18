import { useState } from "react";

export default function EmailCard({ data }) {
  const { email, ai_analysis, heuristic, action } = data;
  const phishing = ai_analysis.is_phishing;
  const [open, setOpen] = useState(false);

  return (
    <article className={`card ${phishing ? "danger" : "safe"}`}>

      {/* STATUS BADGE */}
      <div className="status">
        {phishing ? "🚨 PHISHING" : "✅ SAFE"}
      </div>

      {/* SUBJECT */}
      <h2 className="subject">
        {email.subject || "No subject"}
      </h2>

      {/* META */}
      <div className="meta">
        <span>{email.from}</span>
        <span>{email.date}</span>
      </div>

      {/* CONFIDENCE */}
      <div className="confidence">
        <label>Threat Confidence</label>
        <div className="bar">
          <span style={{ width: `${ai_analysis.confidence}%` }} />
        </div>
        <small>{ai_analysis.confidence}%</small>
      </div>

      {/* SUMMARY */}
      <p className="summary">
        {ai_analysis.summary}
      </p>

      {/* TACTICS */}
      {ai_analysis.tactics?.length > 0 && (
        <div className="tags">
          {ai_analysis.tactics.map((t, i) => (
            <span key={i}>{t}</span>
          ))}
        </div>
      )}

      {/* TOGGLE */}
      <button className="toggle" onClick={() => setOpen(!open)}>
        {open ? "Hide Analysis ▲" : "View Full Analysis ▼"}
      </button>

      {/* DETAILS */}
      {open && (
        <div className="details">
          <section>
            <h4>AI Explanation</h4>
            <p>{ai_analysis.explanation}</p>
          </section>

          <section>
            <h4>Heuristic Signals</h4>
            <ul>
              {heuristic.reasons.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </section>

          <footer>
            Action Taken: <strong>{action}</strong>
          </footer>
        </div>
      )}
    </article>
  );
}