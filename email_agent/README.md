# Project 03 — Autonomous Email Intelligence Agent

An AI-powered email triage system that fetches unread emails, classifies intent
and urgency, drafts professional replies, and presents everything in a
human-in-the-loop review queue.

## Architecture

| Layer | Responsibility |
|-------|---------------|
| **FastAPI API** | REST endpoints for email processing |
| **EmailAgent** | Orchestrates fetch → classify → draft pipeline |
| **Tools** | SRP modules: `GmailFetchTool`, `ClassifyTool`, `DraftTool` |
| **Services** | `GmailClient` / `MockEmailClient` behind `BaseEmailClient` ABC |
| **Frontend** | Streamlit review queue with approve/reject buttons |

## Quick Start

```bash
cd email_agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add your OPENAI_API_KEY
```

### Run the API (uses MockEmailClient by default)

```bash
uvicorn app.main:app --reload --port 8000
```

### Run the Streamlit UI

```bash
streamlit run frontend/streamlit_app.py
```

### Run Tests

```bash
pytest tests/ -v
```

## Gmail OAuth Setup

To use real Gmail integration:

1. Create a Google Cloud project and enable the Gmail API.
2. Download OAuth 2.0 credentials and save as `credentials/client_secret.json`.
3. Run the OAuth flow to generate `credentials/token.json`.
4. Set `GMAIL_CREDENTIALS_PATH=./credentials/token.json` in `.env`.

Until credentials are configured the app falls back to `MockEmailClient`,
which returns realistic sample emails for demonstration purposes.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/emails` | Fetch, classify, and draft replies for unread emails |
| `POST` | `/emails/{id}/approve` | Approve a draft reply (triggers send) |
| `POST` | `/emails/{id}/reject` | Reject a draft, flag for manual handling |

## SOLID Design

- **SRP** — Each tool does exactly one thing.
- **Open/Closed** — Add new intent handlers by adding tools, not editing the agent.
- **Liskov** — `MockEmailClient` substitutes for `GmailClient` transparently.
- **Interface Segregation** — Agent receives clean email dicts, never touches OAuth.
- **Dependency Inversion** — Agent is injected with tools at init time.
