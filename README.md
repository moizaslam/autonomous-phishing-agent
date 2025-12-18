# Autonomous Phishing Agent

An **AI-powered autonomous cybersecurity system** that scans inbox emails, detects phishing and social-engineering attacks, and provides clear, explainable threat analysis using both AI models and heuristic rules.

This project is built as an **academic and practical cybersecurity solution** with a strong focus on **reliability, explainability, and safe failure handling**.

---

## 🚀 Features

* Autonomous email scanning
* AI-based phishing detection
* Automatic AI fallback system
* Heuristic threat analysis (links, domains, sender trust)
* Confidence-based risk scoring
* Explainable AI output
* Modern, responsive frontend dashboard
* Safe-by-design architecture (no silent failures)

---

## 🧠 How the System Works

1. The system connects to the email inbox and fetches unseen emails.
2. Each email is analyzed using:

   * AI models (DeepSeek / Hugging Face)
   * Heuristic phishing rules
3. If the AI fails (quota exceeded, API error, empty response):

   * The system automatically falls back to heuristic analysis.
4. Results are normalized into a unified report.
5. The frontend displays:

   * **SAFE** or **PHISHING** status
   * Confidence percentage
   * AI explanation
   * Heuristic indicators
   * Final action taken

---

## 🧰 Tech Stack

### Backend

* Python
* Flask (REST API)
* Email via IMAP / Gmail
* **AI Providers**:

  * DeepSeek (primary)
  * Hugging Face (fallback)
* Heuristic phishing engine
* Defensive JSON parsing

### Frontend

* React (Vite)
* Plain CSS (no Tailwind)
* Responsive UI
* Expandable email analysis cards

---

## 📁 Project Structure

```
autonomous-phishing-agent
│
├── backend
│   ├── app.py                 # Flask API entry point
│   ├── email_monitor.py       # Fetches unseen emails
│   ├── summarizer.py          # AI analysis and fallback logic
│   ├── phishing_detector.py   # Heuristic scoring engine
│   ├── reporter.py            # Final normalized report
│   ├── processed_ids.py       # Prevents duplicate scans
│   ├── config.py              # Environment configuration
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── components
│   │       └── EmailCard.jsx
│   └── package.json
│
└── README.md
```

---

## 🔐 Environment Setup

Create a `.env` file inside the **backend** directory:

```env
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password

HF_API_TOKEN=your_huggingface_token
```

### Important

* **Do not commit** the `.env` file
* All secrets are excluded using `.gitignore`

---

## ▶️ Running the Project

### Clone the Repository

```bash
git clone git@github.com:moizaslam/autonomous-phishing-agent.git
cd autonomous-phishing-agent
```

---

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

Backend runs on:

```
http://127.0.0.1:5000
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## 🛡️ Safety & Reliability

* No crashes when AI services fail
* No empty or partial AI responses
* Defensive handling of null values
* Explicit fallback logging
* Always returns a valid analysis result

---

## 🎓 Academic Relevance

This project demonstrates:

* Applied cybersecurity engineering
* Explainable AI (XAI)
* AI reliability under failure conditions
* Secure software design
* Real-world system architecture

### Suitable for

* University final year projects
* Cybersecurity coursework
* AI safety and reliability demonstrations

---

## 👤 Author

**Muhammad Moiz Aslam**
Senior Frontend & Full-Stack Developer
Cybersecurity & AI Enthusiast

GitHub: [https://github.com/moizaslam]