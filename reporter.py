import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def send_phishing_alert(email_data, heuristic, ai_analysis):
    msg = MIMEMultipart()
    msg["From"] = Config.EMAIL_USER
    msg["To"] = Config.ADMIN_EMAIL
    msg["Subject"] = "🚨 Phishing Alert Detected"

    body = f"""
PHISHING ALERT 🚨

Sender:
{email_data['from']}

Subject:
{email_data['subject']}

Detected URLs:
{", ".join(heuristic.get("urls", []))}

Heuristic Risk Score:
{heuristic.get("score")}

AI Verdict:
Phishing: {ai_analysis.get("is_phishing")}
Confidence: {ai_analysis.get("confidence")}%

Summary:
{ai_analysis.get("summary")}

Explanation:
{ai_analysis.get("explanation")}

--- 
This alert was generated automatically by the Autonomous Phishing Agent.
"""

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()
