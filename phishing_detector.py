import re

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "account",
    "suspended",
    "limited",
    "click",
    "login",
    "password",
    "confirm",
    "security alert",
]

TRUSTED_DOMAINS = ["google.com", "paypal.com", "microsoft.com", "apple.com"]


def extract_urls(text):
    url_regex = r"https?://[^\s]+"
    return re.findall(url_regex, text)


def sender_domain(sender):
    if not sender or "@" not in sender:
        return ""
    return sender.split("@")[-1].replace(">", "").lower()


def phishing_score(email_data):
    score = 0
    reasons = []

    text = f"{email_data['subject']} {email_data['body']}".lower()

    # Keyword check
    for word in SUSPICIOUS_KEYWORDS:
        if word in text:
            score += 1
            reasons.append(f"Suspicious keyword: {word}")

    # URL check
    urls = extract_urls(text)
    if urls:
        score += 2
        reasons.append("Contains URL(s)")

    # Sender domain check
    domain = sender_domain(email_data.get("from", ""))
    if domain and not any(domain.endswith(td) for td in TRUSTED_DOMAINS):
        score += 2
        reasons.append(f"Untrusted sender domain: {domain}")

    return {
        "score": score,
        "urls": urls,
        "reasons": reasons,
        "is_suspicious": score >= 3,
    }
