from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from email_monitor import fetch_unread_emails, mark_as_seen
from phishing_detector import phishing_score
from summarizer import analyze_email_with_ai
from reporter import send_phishing_alert
from processed_ids import load_processed, save_processed

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Trusted domains
TRUSTED_DOMAINS = [
    "google.com",
    "accounts.google.com",
    "linkedin.com",
    "pinterest.com",
    "explore.pinterest.com",
    "mustakbil.com",
    "instagram.com",
    "facebook.com",
    "facebookmail.com",
    "github.com",
    "stackoverflow.com",
    "medium.com",
]


def is_trusted_sender(sender: str) -> bool:
    if not sender:
        return False
    sender = sender.lower()
    return any(domain in sender for domain in TRUSTED_DOMAINS)


def enforce_ai_fields(ai_result: dict) -> dict:
    """
    Ensure summary and explanation are never empty.
    """
    if not ai_result.get("summary"):
        ai_result["summary"] = (
            "The email was analyzed and contains a message directed to the recipient."
        )

    if not ai_result.get("explanation"):
        ai_result["explanation"] = (
            "The system reviewed the sender, content, links, and structure of the email "
            "to determine whether it appears safe or suspicious."
        )

    ai_result.setdefault("confidence", 0)
    ai_result.setdefault("tactics", [])
    ai_result.setdefault("is_phishing", False)

    return ai_result


@app.route("/")
def home():
    return jsonify(
        {
            "status": "running",
            "service": "Autonomous Phishing Email Analyzer & Reporter",
        }
    )


@app.route("/agent/run")
def run_agent():
    emails = fetch_unread_emails()
    processed_ids = load_processed()

    results = []
    newly_processed = set()

    for email_data in emails:
        msg_id = email_data.get("message_id") or email_data.get("id")

        # Skip already processed
        if not msg_id or msg_id in processed_ids:
            continue

        heuristic = phishing_score(email_data)
        sender = email_data.get("from", "")

        # ─────────────────────────────────────
        # Trusted sender → AI summary, forced safe
        # ─────────────────────────────────────
        if is_trusted_sender(sender):
            ai_result = analyze_email_with_ai(email_data, heuristic)
            ai_result = enforce_ai_fields(ai_result)

            ai_result["is_phishing"] = False
            ai_result["confidence"] = max(ai_result.get("confidence", 0), 70)
            ai_result["explanation"] = "Sender domain is trusted."

            results.append(
                {
                    "email": email_data,
                    "heuristic": heuristic,
                    "ai_analysis": ai_result,
                    "action": "No action",
                }
            )

            newly_processed.add(msg_id)
            mark_as_seen(email_data["id"])
            continue

        # ─────────────────────────────────────
        # Low-risk email → AI summary, safe verdict
        # ─────────────────────────────────────
        if heuristic["score"] < 4:
            ai_result = analyze_email_with_ai(email_data, heuristic)
            ai_result = enforce_ai_fields(ai_result)

            ai_result["is_phishing"] = False
            ai_result["confidence"] = heuristic["score"] * 5

            results.append(
                {
                    "email": email_data,
                    "heuristic": heuristic,
                    "ai_analysis": ai_result,
                    "action": "No action",
                }
            )

            newly_processed.add(msg_id)
            mark_as_seen(email_data["id"])
            continue

        # ─────────────────────────────────────
        # Suspicious email → AI + possible alert
        # ─────────────────────────────────────
        ai_result = analyze_email_with_ai(email_data, heuristic)
        ai_result = enforce_ai_fields(ai_result)

        ai_result["confidence"] = min(
            int((heuristic["score"] * 10 + ai_result.get("confidence", 0)) / 2),
            100,
        )

        if ai_result.get("is_phishing"):
            send_phishing_alert(email_data, heuristic, ai_result)

        results.append(
            {
                "email": email_data,
                "heuristic": heuristic,
                "ai_analysis": ai_result,
                "action": "Alert sent" if ai_result.get("is_phishing") else "No action",
            }
        )

        newly_processed.add(msg_id)
        mark_as_seen(email_data["id"])

    # ─────────────────────────────────────
    # No new emails
    # ─────────────────────────────────────
    if not results:
        return jsonify(
            {
                "status": "idle",
                "message": "No new unseen emails to process.",
                "results": [],
            }
        )

    # Persist processed IDs
    save_processed(processed_ids | newly_processed)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
