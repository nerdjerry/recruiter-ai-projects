# Feedback Classifier

Sentiment-aware customer feedback classifier powered by an LLM, with a FastAPI
backend and Streamlit dashboard.

## Setup

```bash
cd feedback_classifier
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add your OpenAI key
```

## Run

```bash
# API server
uvicorn app.main:app --reload

# Streamlit dashboard (in a second terminal)
streamlit run frontend/streamlit_app.py
```

## Tests

```bash
pytest tests/ -v
```

## Project highlights

| SOLID principle | Where |
|---|---|
| **SRP** | `classifier.py`, `prioritizer.py`, `storage.py` each own one responsibility |
| **Open/Closed** | `BaseExporter` → add new formats without touching existing exporters |
| **Liskov** | CSV, JSON, Markdown exporters are interchangeable via `BaseExporter.export()` |
| **ISP** | Dashboard uses `FeedbackSummary`, not the full storage model |
| **DIP** | `ClassificationService` receives its prompt template as a parameter |
