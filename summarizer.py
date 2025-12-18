from huggingface_hub import InferenceClient
from config import Config
import re

client = InferenceClient(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    token=Config.HF_API_TOKEN,
)


def truncate_text(text, max_chars=1500):
    return text[:max_chars] if text else ""


def analyze_email_with_ai(email_data, heuristic):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior cybersecurity analyst. "
                        "Analyze emails carefully and be specific. "
                        "Do not give generic answers."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
From: {email_data['from']}
Subject: {email_data['subject']}
Body:
{truncate_text(email_data['body'])}

Explain:
1. What the email is about
2. Whether it is phishing or legitimate
3. Why
""",
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )

        text = response.choices[0].message.content.strip()

        if len(text) < 50:
            raise ValueError("AI response too short")

        return interpret_response(text, heuristic)

    except Exception as e:
        print("❌ HF API fallback triggered:", e)
        return fallback_analysis(heuristic)


def interpret_response(text, heuristic):
    lower = text.lower()

    # AI-driven phishing decision (not heuristic-driven)
    phishing = any(
        phrase in lower
        for phrase in [
            "this is a phishing",
            "phishing email",
            "scam",
            "fraud",
            "attempts to deceive",
            "malicious",
        ]
    )

    # Confidence
    if phishing:
        confidence = min(75 + heuristic["score"] * 5, 95)
    else:
        confidence = max(20, heuristic["score"] * 5)

    # Summary = first 2 sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:2]).strip()

    # Tactics
    tactics = []
    if "link" in lower or heuristic.get("urls"):
        tactics.append("link manipulation")
    if "impersonat" in lower:
        tactics.append("impersonation")
    if "credential" in lower or "password" in lower:
        tactics.append("credential harvesting")
    if "urgent" in lower:
        tactics.append("urgency")

    return {
        "is_phishing": phishing,
        "confidence": confidence,
        "summary": summary,
        "tactics": tactics,
        "explanation": text,
    }


def fallback_analysis(heuristic):
    return {
        "is_phishing": heuristic["score"] >= 5,
        "confidence": min(heuristic["score"] * 10, 80),
        "summary": "AI analysis could not be completed.",
        "tactics": [],
        "explanation": "The AI service was unavailable, so a heuristic-based assessment was used.",
    }
