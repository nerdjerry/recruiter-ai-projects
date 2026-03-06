# AI Student Project Specs
### 5 AI projects · Personal scale · Enterprise principles · SOLID architecture

These specs are written to pass directly to an AI coding assistant (Copilot, Cursor, or similar). Each spec defines folder structure, SOLID design notes, API contracts, environment variables, and extension ideas. Projects are scoped at the personal/portfolio level — no enterprise auth, multi-tenancy, or production infra required — but follow clean architecture patterns that scale.

| | |
|---|---|
| **Audience** | Students building AI portfolio projects (beginner to intermediate) |
| **Philosophy** | Personal scale, enterprise principles — SOLID applied at a readable level |
| **Language** | Python 3.11+ · FastAPI backend · Streamlit frontend |
| **LLM Provider** | OpenAI API (GPT-4o / GPT-4o-mini) — swap for Anthropic or open-source as needed |

---

## Projects

| # | Project | Tier | Key Concepts |
|---|---------|------|--------------|
| 01 | [AI-Powered Resume Screener](projects/01-resume-screener.md) | Tier 1 — Beginner | Parsing, Embeddings, Semantic Scoring |
| 02 | [Sentiment-Aware Customer Feedback Classifier](projects/02-feedback-classifier.md) | Tier 1 — Beginner | Classification, Priority Scoring, SQLite |
| 03 | [Autonomous Email Intelligence Agent](projects/03-email-agent.md) | Tier 2 — Intermediate | Tool Calling, Gmail API, Human-in-the-Loop |
| 04 | [Real-Time Research Copilot](projects/04-research-copilot.md) | Tier 2 — Intermediate | Tool Calling, RAG, FAISS, Confidence Scoring |
| 05 | [Personal Finance Agent with Memory](projects/05-finance-agent.md) | Tier 3 — Advanced | Memory Architecture, Plaid API, Proactive Insights |

> Start with Project 01 or 02 (Tier 1) before attempting the agent-based projects.
> Each project builds on concepts from the previous — parsers → tool calling → memory.

---

## How to Use With Copilot

Copy the folder structure and SOLID notes for your chosen project and use this prompt template:

```
I'm building [PROJECT NAME] as a student portfolio project.
Here is the folder structure I want to follow: [PASTE]
Here are the SOLID design constraints: [PASTE]
Here are the API endpoints I need: [PASTE]

Please scaffold the project, starting with:
  1. The Pydantic schemas in models/schemas.py
  2. The core service files
  3. The FastAPI router

Use dependency injection and keep each file under 100 lines.
```