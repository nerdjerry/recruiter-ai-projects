# PROJECT 01 — AI-Powered Resume Screener
> **Tier 1 — Beginner Friendly**
> `Python` · `OpenAI API` · `LangChain` · `FastAPI` · `FAISS` · `Streamlit`

**One line:** Match resumes to job descriptions using semantic scoring and LLM-generated explanations.

A web app where a recruiter pastes a job description, uploads one or multiple resumes (PDF/DOCX), and receives a ranked shortlist with match scores, skill gap analysis, and a plain-English explanation of each decision. No enterprise auth, no multi-tenant infra — just clean, well-structured code.

### Goals
- Parse resume and JD text from uploaded files
- Generate a semantic similarity score using embeddings
- Use an LLM to explain the score in plain English
- Rank candidates and display a summary table

### Folder Structure

```
resume_screener/
  app/
    main.py               # FastAPI entry point
    routers/
      screening.py        # POST /screen endpoint
    services/
      parser.py           # Resume/JD text extraction (SRP)
      embedder.py         # Embedding + similarity (SRP)
      scorer.py           # Score + LLM explanation (SRP)
    models/
      schemas.py          # Pydantic input/output models
    core/
      config.py           # Env-based config (no hardcoded keys)
  frontend/
    streamlit_app.py      # UI calling the FastAPI backend
  tests/
    test_parser.py
    test_scorer.py
  .env.example
  requirements.txt
  README.md
```

### SOLID Design Notes

| Principle | How it applies in this project |
|---|---|
| **S — Single Responsibility** | `parser.py` only extracts text. `embedder.py` only handles vectors. `scorer.py` only calls the LLM. |
| **O — Open/Closed** | Add a new file type parser (e.g., DOCX) by adding a new class, not modifying existing ones. |
| **L — Liskov Substitution** | All parsers implement a `BaseParser` interface with a `parse(file) -> str` method. |
| **I — Interface Segregation** | `Scorer` does not depend on the embedder directly — it receives a pre-computed score float. |
| **D — Dependency Inversion** | Services receive config via constructor injection, not `os.getenv()` inside functions. |

### API Endpoints

```
POST /screen   — Accepts JD text + resume files, returns ranked list with scores and explanations
GET  /health   — Basic health check
```

### Environment Variables

```
OPENAI_API_KEY
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
MAX_UPLOAD_MB=5
```

### Extension Ideas
- Add a bias-aware scoring flag that prompts the LLM to flag demographic proxies
- Plug in a vector DB (Pinecone/Chroma) to persist and search past screenings
- Add a feedback loop: recruiter marks shortlist → fine-tune scoring weights
