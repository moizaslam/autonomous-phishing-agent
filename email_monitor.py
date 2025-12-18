import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from config import Config


def clean_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.replace("\r", "").replace("\n", " ").split())


def connect_to_mailbox():
    mail = imaplib.IMAP4_SSL(Config.EMAIL_HOST, Config.EMAIL_PORT)
    mail.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
    mail.select("INBOX")
    return mail


def mark_as_seen(email_id: str):
    """
    Mark a single email as SEEN.
    """
    mail = connect_to_mailbox()
    try:
        mail.store(email_id, "+FLAGS", "\\Seen")
    finally:
        mail.logout()


def extract_email_body(msg) -> str:
    """
    Prefer text/plain, fallback to cleaned text/html.
    """
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))

            if content_type == "text/plain" and "attachment" not in disposition:
                body = part.get_payload(decode=True).decode(errors="ignore")
                break

            if content_type == "text/html" and not body:
                html = part.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html, "lxml")
                body = soup.get_text(separator=" ", strip=True)
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True).decode(errors="ignore")

        if content_type == "text/html":
            soup = BeautifulSoup(payload, "lxml")
            body = soup.get_text(separator=" ", strip=True)
        else:
            body = payload

    return clean_text(body)


def fetch_unread_emails(limit=10, days=7):
    """
    Fetch UNSEEN emails from the last `days`.
    """
    mail = connect_to_mailbox()

    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(UNSEEN SINCE "{since_date}")')

    if status != "OK" or not messages[0]:
        mail.logout()
        return []

    email_ids = messages[0].split()[-limit:]
    emails = []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # ---- SUBJECT ----
        subject, encoding = decode_header(msg.get("Subject"))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        # ---- DATE (SAFE & NORMALIZED) ----
        email_date_raw = msg.get("Date")
        try:
            email_date = parsedate_to_datetime(email_date_raw)
            if email_date.tzinfo is None:
                email_date = email_date.replace(tzinfo=timezone.utc)
            else:
                email_date = email_date.astimezone(timezone.utc)
        except Exception:
            email_date = None

        # HARD FILTER → skip old emails
        if email_date and email_date < cutoff_date:
            continue

        # ---- BODY ----
        body = extract_email_body(msg)

        emails.append(
            {
                "id": email_id.decode(),
                "message_id": msg.get("Message-ID"),
                "from": msg.get("From"),
                "subject": clean_text(subject),
                "body": body,
                "date": email_date_raw,
            }
        )

    mail.logout()
    return emails
