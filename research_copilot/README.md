# 🔬 Research Copilot

A Real-Time Research Copilot that synthesises answers from multiple sources
(web search, Wikipedia, private knowledge base) using direct OpenAI calls —
no LangChain required.

## Quick Start

```bash
cd research_copilot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your API keys
```

### Run the API

```bash
uvicorn app.main:app --reload
```

### Run the Frontend

```bash
streamlit run frontend/streamlit_app.py
```

### Run Tests

```bash
pytest tests/ -v
```

## Architecture

| Layer | Responsibility |
|-------|---------------|
| `routers/` | HTTP endpoints (FastAPI) |
| `agents/` | Orchestration — calls tools, synthesises answer |
| `tools/` | One tool per external source (SRP) |
| `services/` | Vector store & confidence scoring |
| `models/` | Pydantic v2 schemas |
| `core/` | Config & prompt templates |

## SOLID Principles

- **SRP** — each tool wraps exactly one source; confidence only scores.
- **Open/Closed** — add a new tool class (e.g. ArXiv) without modifying the agent.
- **LSP** — all tools implement `BaseTool.run(query) → list[ToolResult]`.
- **ISP** — `ConfidenceService` only consumes the final answer + sources list.
- **DIP** — the agent receives its tool list via constructor injection.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `TAVILY_API_KEY` | Tavily search API key |
| `CHAT_MODEL` | Chat model name (default: `gpt-4o`) |
| `EMBEDDING_MODEL` | Embedding model (default: `text-embedding-3-small`) |
| `VECTORSTORE_PATH` | Path for vector store data |
