# Autonomous Phishing Agent

An AI-powered autonomous system that monitors emails, detects phishing and social engineering attempts, and provides clear explanations using both AI and heuristic analysis.

This project is designed as an **academic + practical cybersecurity solution**, combining machine intelligence with rule-based safety mechanisms.

---

## Features

- 📥 **Autonomous Email Scanning**
- 🧠 **AI-Based Phishing Detection**
- 🔁 **Automatic AI Fallback System**
- 🔍 **Heuristic Analysis (Links, Domains, Sender Trust)**
- 📊 **Threat Confidence Scoring**
- 🧾 **Explainable AI Results**
- 🌐 **Modern Frontend Dashboard**
- 🔒 **Safe-by-Design (No silent failures)**

---

## How the System Works

1. Emails are fetched from the inbox
2. Each email is analyzed using:
   - AI models (DeepSeek / HuggingFace)
   - Heuristic phishing rules
3. If AI fails (quota, error, empty response):
   - System automatically falls back to heuristics
4. Results are normalized and returned to the frontend
5. UI displays:
   - SAFE / PHISHING status
   - Confidence score
   - AI explanation
   - Heuristic signals
   - Final action taken

---

## Tech Stack

### Backend
- Python
- Flask (REST API)
- Gmail API
- AI Providers:
  - DeepSeek (primary)
  - HuggingFace (fallback)
- Heuristic Engine
- JSON-based state tracking

### Frontend
- React (Vite)
- Plain CSS (no Tailwind)
- Responsive UI
- Expandable email analysis cards

---

## Core Modules

| File | Purpose |
|-----|--------|
| `email_monitor.py` | Fetches unseen emails |
| `summarizer.py` | AI analysis + fallback logic |
| `phishing_detector.py` | Heuristic scoring |
| `reporter.py` | Final threat report |
| `processed_ids.py` | Prevents duplicate scans |
| `app.py` | Flask API |
| `EmailCard.jsx` | Email UI component |

---

## Safety & Reliability

- No crashes on AI failure
- No empty AI responses
- Defensive parsing (`None` safe)
- Explicit fallback logging
- Always returns a valid result

---

## Running the Project

### Backend
```bash
python app.py

### Frontend
```bash
npm install
npm run dev

👤 Author

Muhammad Moiz Aslam
Senior Frontend & Full-Stack Developer
Cybersecurity & AI Enthusiast