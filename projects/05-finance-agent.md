# PROJECT 05 — Personal Finance Agent with Memory
> **Tier 3 — Advanced (Memory + Tool Calling)**
> `Python` · `OpenAI API` · `Plaid API` · `SQLite` · `Streamlit`

**One line:** A money-aware agent that tracks your spending patterns, remembers your goals, and surfaces insights unprompted.

A personal finance assistant that connects to transaction data (via Plaid sandbox or CSV upload), remembers the user's financial goals and past conversations across sessions, and proactively surfaces spending insights without being asked every time. Memory architecture is the core differentiator: the agent stores facts, goals, and behavioral patterns in both short-term (session) and long-term (persistent) memory.

### Goals
- Ingest transaction data (Plaid sandbox or CSV fallback)
- Maintain long-term memory of user goals, budgets, and preferences
- Maintain short-term session memory for conversation continuity
- Answer financial questions grounded in real transaction data
- Proactively surface weekly insights without explicit prompting

### Folder Structure

```
finance_agent/
  app/
    main.py
    routers/
      chat.py             # POST /chat  (conversational endpoint)
      transactions.py     # POST /sync, GET /transactions
      insights.py         # GET /insights/weekly
    agents/
      finance_agent.py    # LangChain agent with memory injection
    tools/
      spending_tool.py    # Query + aggregate transactions (SRP)
      budget_tool.py      # Check budget status vs. goals (SRP)
      insight_tool.py     # Generate proactive insight text (SRP)
    memory/
      short_term.py       # ConversationBufferMemory wrapper
      long_term.py        # Mem0 or Zep client wrapper
      memory_manager.py   # Coordinates both memory stores (SRP)
    services/
      plaid_client.py     # Plaid sandbox API client
      csv_importer.py     # Fallback CSV transaction ingestion
      categorizer.py      # LLM-based transaction categorization
    models/
      schemas.py
    core/
      config.py
      prompts.py
  frontend/
    streamlit_app.py      # Chat UI + spending dashboard
  tests/
  data/
    transactions.db
  .env.example
```

### SOLID Design Notes

| Principle | How it applies in this project |
|---|---|
| **S — Single Responsibility** | `memory_manager.py` is the only place that touches both memory stores. Tools do not manage memory directly. |
| **O — Open/Closed** | Swap Mem0 for Zep by replacing `long_term.py` without touching the agent or any tool. |
| **L — Liskov Substitution** | `PlaidClient` and `CsvImporter` both implement `BaseTransactionSource.fetch(days) -> list[Transaction]`. |
| **I — Interface Segregation** | The chat router depends only on the agent, not on memory internals — memory is fully encapsulated. |
| **D — Dependency Inversion** | `FinanceAgent` receives `memory_manager` and tools via constructor — no static dependencies. |

### API Endpoints

```
POST /chat             — User message → agent reply (memory-aware, grounded in transactions)
POST /sync             — Pull latest transactions from Plaid (or re-import CSV)
GET  /insights/weekly  — Returns proactive weekly summary without user prompt
DELETE /memory         — Clear user memory (privacy reset)
```

### Environment Variables

```
OPENAI_API_KEY
PLAID_CLIENT_ID
PLAID_SECRET
PLAID_ENV=sandbox
MEM0_API_KEY
CHAT_MODEL=gpt-4o
DB_PATH=./data/transactions.db
```

### Extension Ideas
- Add anomaly detection: alert when a category spends 2× above 30-day average
- Build a goal-setting flow where the agent saves goals to long-term memory and tracks progress
- Swap Plaid for a manual CSV import to make it fully free and privacy-safe for demo use
