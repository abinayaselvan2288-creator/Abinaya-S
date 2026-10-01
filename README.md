# PocketSmart AI

PocketSmart AI is a Generative AI powered budget and recommendation assistant.

It provides:

- Home Interior Budget Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional Outfit Image Analysis
- Gemini AI Integration
- User Registration
- User Login
- JWT Authentication
- Recommendation History
- Platform Search Links
- Responsive Web Interface

---

# Technology Stack

## Frontend

- HTML
- CSS
- JavaScript
- Jinja2

## Backend

- Python
- FastAPI
- Uvicorn

## AI

- Google Gemini API
- google-genai Python SDK

## Database

- SQLite

## Authentication

- JWT
- bcrypt password hashing

---

# Project Structure

```text
PocketSmart-AI/

├── app/

│   ├── __init__.py

│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── schemas.py
│   ├── dependencies.py

│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── planners.py
│   │   ├── history.py
│   │   └── pages.py

│   ├── services/
│   │   ├── __init__.py
│   │   ├── catalog.py
│   │   └── gemini_service.py

│   ├── templates/
│   │   ├── index.html
│   │   └── app.html

│   └── static/
│       ├── style.css
│       └── app.js

├── tests/
│   └── test_smoke.py

├── .env.example
├── .gitignore
├── requirements.txt
└── README.md