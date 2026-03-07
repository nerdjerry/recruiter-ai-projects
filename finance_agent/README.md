# Project 05 — Personal Finance Agent with Memory

A conversational AI agent that helps you understand your spending, track budgets, and get proactive financial insights — powered by OpenAI, FastAPI, and Streamlit.

## Features

- **Chat** — Ask natural-language questions about your finances
- **Memory** — The agent remembers your budget goals and conversation history
- **CSV Import** — Upload bank transaction CSVs as a Plaid-free fallback
- **Weekly Insights** — Proactive AI-generated spending summaries
- **Transaction Browsing** — Filter and explore your transaction history

## Architecture (SOLID)

| Principle | Implementation |
|---|---|
| **SRP** | `MemoryManager` is the sole coordinator for both memory stores. Tools don't manage memory. |
| **Open/Closed** | Swap `JsonLongTermMemory` for Mem0/Zep by subclassing `BaseLongTermMemory` — no agent changes. |
| **Liskov** | `PlaidClient` and `CsvImporter` both implement `BaseTransactionSource.fetch()`. |
| **ISP** | Chat router depends only on the agent, not memory internals. |
| **DI** | `FinanceAgent` receives all dependencies (memory, tools, config) via constructor. |

## Quick Start

### 1. Install dependencies

```bash
cd finance_agent
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

### 4. Run the Streamlit UI

```bash
streamlit run frontend/streamlit_app.py
```

### 5. Run tests

```bash
pytest tests/ -v
```

## Sample CSV Format

Upload a CSV file with these columns:

```csv
date,description,amount
2024-01-15,Grocery Store,45.50
2024-01-16,Gas Station,30.00
2024-01-17,Netflix Subscription,15.99
2024-01-18,Electric Bill,120.00
```

An optional `category` column is also supported:

```csv
date,description,amount,category
2024-01-15,Grocery Store,45.50,food
```

If no category is provided, the agent will auto-categorize using the LLM.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Send a message, get an AI reply with memory context |
| `DELETE` | `/memory` | Clear all user memory (privacy reset) |
| `POST` | `/sync` | Upload a CSV file to import transactions |
| `GET` | `/transactions` | List transactions with optional filters |
| `GET` | `/insights/weekly` | Get a proactive weekly spending summary |
| `GET` | `/health` | Health check |

## Note on Plaid

The `PlaidClient` class is included but raises `NotImplementedError` by default. The **CSV importer is the working default** — no Plaid credentials are needed. To enable Plaid, implement the `fetch()` method with your sandbox credentials.
