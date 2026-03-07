# PROJECT 03 — Autonomous Email Intelligence Agent
> **Tier 2 — Intermediate (Tool Calling)**
> `Python` · `OpenAI API` · `Gmail API` · `FastAPI` · `Streamlit`

**One line:** Read, classify, and draft intelligent replies to emails using LLM-powered intent detection.

An agent that connects to a Gmail inbox (via OAuth), reads new emails, detects intent and urgency, generates a proposed reply, and flags anything requiring human review. The agent never sends without human approval — an important design constraint that shows responsible AI thinking.

### Goals
- Authenticate with Gmail via OAuth 2.0
- Read and parse recent unread emails
- Classify intent (inquiry / complaint / scheduling / spam / other)
- Draft a context-aware reply using the LLM
- Surface a review queue — human approves before any send

### Folder Structure

```
email_agent/
  app/
    main.py
    routers/
      emails.py           # GET /emails, POST /emails/{id}/approve
    agents/
      email_agent.py      # LangChain agent orchestration
    tools/
      gmail_tool.py       # Tool: fetch emails (SRP)
      draft_tool.py       # Tool: generate draft reply (SRP)
      classify_tool.py    # Tool: classify intent (SRP)
    services/
      gmail_client.py     # Gmail API wrapper
    models/
      schemas.py          # Email, DraftReply, Classification
    core/
      config.py
      prompts.py
  frontend/
    streamlit_app.py      # Review queue UI
  tests/
  credentials/            # gitignored OAuth token
  .env.example
```

### SOLID Design Notes

| Principle | How it applies in this project |
|---|---|
| **S — Single Responsibility** | Each LangChain tool does one thing: fetch, classify, or draft. The agent just orchestrates. |
| **O — Open/Closed** | Add a new intent handler (e.g., auto-schedule meetings) by adding a new tool, not modifying the agent loop. |
| **L — Liskov Substitution** | A mock `GmailClient` can replace the real one in tests — both implement the same `BaseEmailClient`. |
| **I — Interface Segregation** | The agent doesn't know about OAuth — it only receives clean email dicts from the client. |
| **D — Dependency Inversion** | Agent is injected with tools at init time, not hardcoded — easy to swap or extend. |

### API Endpoints

```
GET  /emails              — Fetch unread emails with classification and draft
POST /emails/{id}/approve — Mark draft approved (triggers send)
POST /emails/{id}/reject  — Discard draft, flag for manual handling
```

### Environment Variables

```
OPENAI_API_KEY
GMAIL_CREDENTIALS_PATH=./credentials/token.json
CHAT_MODEL=gpt-4o
MAX_EMAILS_PER_RUN=20
HUMAN_IN_THE_LOOP=true
```

### Extension Ideas
- Add short-term conversation memory so follow-up replies maintain thread context
- Connect to a calendar API tool to auto-propose meeting slots
- Build an Outlook variant by swapping the email client class
