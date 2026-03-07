# AI Student Project Specs
### 5 AI projects · Personal scale · Enterprise principles · SOLID architecture

Five fully-built AI portfolio projects with FastAPI backends, Streamlit frontends, and comprehensive test suites. Each project follows SOLID design principles with clean architecture that scales.

| | |
|---|---|
| **Audience** | Students building AI portfolio projects (beginner to intermediate) |
| **Philosophy** | Personal scale, enterprise principles — SOLID applied at a readable level |
| **Language** | Python 3.11+ · FastAPI backend · Streamlit frontend |
| **LLM Provider** | OpenAI API (GPT-4o / GPT-4o-mini) — swap for Anthropic or open-source as needed |

---

## Projects

| # | Project | Directory | Tier | Key Concepts |
|---|---------|-----------|------|--------------|
| 01 | [AI-Powered Resume Screener](projects/01-resume-screener.md) | [`resume_screener/`](resume_screener/) | Tier 1 — Beginner | Parsing, Embeddings, Semantic Scoring |
| 02 | [Sentiment-Aware Feedback Classifier](projects/02-feedback-classifier.md) | [`feedback_classifier/`](feedback_classifier/) | Tier 1 — Beginner | Classification, Priority Scoring, SQLite |
| 03 | [Email Intelligence Agent](projects/03-email-agent.md) | [`email_agent/`](email_agent/) | Tier 2 — Intermediate | Tool Calling, Gmail API, Human-in-the-Loop |
| 04 | [Real-Time Research Copilot](projects/04-research-copilot.md) | [`research_copilot/`](research_copilot/) | Tier 2 — Intermediate | Tool Calling, RAG, Vector Search, Confidence Scoring |
| 05 | [Personal Finance Agent](projects/05-finance-agent.md) | [`finance_agent/`](finance_agent/) | Tier 3 — Advanced | Memory Architecture, CSV/Plaid, Proactive Insights |

> Start with Project 01 or 02 (Tier 1) before attempting the agent-based projects.
> Each project builds on concepts from the previous — parsers → tool calling → memory.

---

## Quick Start

Each project is self-contained. To run any project:

```bash
# 1. Navigate to the project directory
cd resume_screener  # or feedback_classifier, email_agent, etc.

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the FastAPI backend
uvicorn app.main:app --reload --port 8000

# 6. In a separate terminal, run the Streamlit frontend
streamlit run frontend/streamlit_app.py

# 7. Run tests (no API key needed — external calls are mocked)
pytest tests/ -v
```

---

## Project Architecture

Every project follows the same clean architecture pattern:

```
project_name/
  app/
    main.py              # FastAPI entry point + CORS
    routers/             # Route handlers (thin — delegate to services)
    services/            # Business logic (one responsibility per file)
    models/
      schemas.py         # Pydantic v2 input/output models
    core/
      config.py          # pydantic-settings BaseSettings (no hardcoded keys)
      prompts.py         # LLM prompts as constants
  frontend/
    streamlit_app.py     # UI calling the FastAPI backend
  tests/                 # pytest tests with mocked external calls
  .env.example           # Template for environment variables
  requirements.txt       # Project dependencies
  README.md              # Project-specific setup guide
```

### SOLID Principles Applied

| Principle | Pattern Used |
|---|---|
| **Single Responsibility** | One service/tool per file, each doing exactly one thing |
| **Open/Closed** | Abstract base classes (`BaseParser`, `BaseExporter`, `BaseTool`, etc.) allow extension without modification |
| **Liskov Substitution** | Implementations are interchangeable — mock clients work in tests, real clients in production |
| **Interface Segregation** | Routers depend on slim schemas, not full storage models |
| **Dependency Inversion** | All services receive config and dependencies via constructor injection |

---

## Detailed Specs

Each project has a full specification document in the [`projects/`](projects/) directory covering folder structure, SOLID design notes, API contracts, environment variables, and extension ideas.