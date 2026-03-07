# Project 01 — AI-Powered Resume Screener

Screen resumes against a job description using OpenAI embeddings and GPT.

## Setup

```bash
cd resume_screener
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your OPENAI_API_KEY
```

## Run the API

```bash
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`. Check `GET /health` to verify.

## Run the Frontend

```bash
streamlit run frontend/streamlit_app.py
```

## Run Tests

```bash
pytest tests/
```

## Architecture (SOLID)

| Principle | Implementation |
|---|---|
| **SRP** | `parser.py` extracts text, `embedder.py` handles vectors, `scorer.py` calls the LLM |
| **Open/Closed** | Add a new file-type parser by subclassing `BaseParser` and registering it |
| **Liskov** | All parsers implement `BaseParser.parse(file_bytes, filename) -> str` |
| **ISP** | `ScoringService` receives a pre-computed score — no dependency on `EmbeddingService` |
| **DIP** | Services receive `Settings` via constructor injection |
