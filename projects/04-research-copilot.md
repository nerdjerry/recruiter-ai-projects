# PROJECT 04 — Real-Time Research Copilot
> **Tier 2 — Intermediate (Tool Calling + RAG)**
> `Python` · `LangChain` · `OpenAI Functions` · `Tavily API` · `FAISS` · `Streamlit`

**One line:** Ask any question and watch the agent search, retrieve, synthesize, and cite its answer live.

A research assistant that takes a natural language question, autonomously decides which tools to call (web search, document retrieval, Wikipedia, etc.), combines results, and returns a cited, confidence-scored answer. Users can also upload documents to ground answers in private knowledge.

### Goals
- Accept a research question from the user
- Agent autonomously selects and calls tools to gather information
- Synthesize results into a structured answer with citations
- Display a confidence score and reasoning trace
- Allow document upload to extend private knowledge base

### Folder Structure

```
research_copilot/
  app/
    main.py
    routers/
      research.py         # POST /research, POST /documents
    agents/
      research_agent.py   # LangChain agent with tool routing
    tools/
      web_search_tool.py  # Tavily search wrapper (SRP)
      retriever_tool.py   # FAISS vector retrieval (SRP)
      wikipedia_tool.py   # Wikipedia API tool (SRP)
    services/
      vectorstore.py      # Document ingestion + FAISS management
      confidence.py       # Confidence scoring heuristic
    models/
      schemas.py
    core/
      config.py
      prompts.py
  frontend/
    streamlit_app.py      # Question input + streamed answer display
  tests/
  data/
    vectorstore/          # persisted FAISS index
  .env.example
```

### SOLID Design Notes

| Principle | How it applies in this project |
|---|---|
| **S — Single Responsibility** | Each tool wraps one external source. `confidence.py` only handles scoring. The agent only orchestrates. |
| **O — Open/Closed** | Add a new source (e.g., ArXiv API) as a new tool class without modifying the agent loop. |
| **L — Liskov Substitution** | All tools implement `BaseTool.run(query) -> str` — agent can use any tool interchangeably. |
| **I — Interface Segregation** | Confidence scoring only consumes the final answer and sources list, not raw tool outputs. |
| **D — Dependency Inversion** | Agent receives its tool list as a constructor argument — easy to configure per-environment. |

### API Endpoints

```
POST /research    — Question + optional doc IDs → answer, citations, confidence score
POST /documents   — Upload PDF/TXT to add to private knowledge base
GET  /documents   — List indexed documents
```

### Environment Variables

```
OPENAI_API_KEY
TAVILY_API_KEY
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
VECTORSTORE_PATH=./data/vectorstore
```

### Extension Ideas
- Add streaming response output using Server-Sent Events so users see the answer build live
- Layer in episodic memory so the agent recalls past research sessions
- Add a "research mode" toggle: quick (1–2 tools) vs. deep (5+ tools, longer latency)
