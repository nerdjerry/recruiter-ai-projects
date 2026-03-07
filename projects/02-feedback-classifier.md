# PROJECT 02 — Sentiment-Aware Customer Feedback Classifier
> **Tier 1 — Beginner Friendly**
> `Python` · `OpenAI API` · `Pandas` · `FastAPI` · `Streamlit` · `SQLite`

**One line:** Turn raw reviews and support tickets into structured, prioritized product intelligence.

A tool that accepts customer feedback in bulk (CSV upload or single text entry), classifies sentiment (positive / neutral / negative), extracts the core topic or complaint, assigns a priority score, and generates a ranked summary report. Output is both viewable in a dashboard and exportable as CSV.

### Goals
- Accept single feedback entry or bulk CSV upload
- Classify sentiment and extract structured fields via LLM
- Assign a priority score (severity × recency heuristic)
- Display a filterable dashboard and export results

### Folder Structure

```
feedback_classifier/
  app/
    main.py
    routers/
      classify.py         # POST /classify, POST /classify/bulk
    services/
      classifier.py       # LLM classification logic (SRP)
      prioritizer.py      # Priority scoring logic (SRP)
      storage.py          # SQLite read/write (SRP)
    models/
      schemas.py          # FeedbackIn, FeedbackOut Pydantic models
    core/
      config.py
      prompts.py          # All prompts as constants (not inline strings)
  frontend/
    streamlit_app.py
  tests/
  .env.example
  requirements.txt
```

### SOLID Design Notes

| Principle | How it applies in this project |
|---|---|
| **S — Single Responsibility** | `classifier.py` calls the LLM. `prioritizer.py` runs the scoring formula. `storage.py` manages persistence. |
| **O — Open/Closed** | Add a new output format (e.g., JSON export) without modifying existing export logic. |
| **L — Liskov Substitution** | All exporters implement `BaseExporter.export(results)` — CSV, JSON, Markdown all interchangeable. |
| **I — Interface Segregation** | Dashboard UI depends only on a lightweight `FeedbackSummary` schema, not the full storage model. |
| **D — Dependency Inversion** | Classifier accepts a prompt template as a parameter, not hardcoded inside the function. |

### API Endpoints

```
POST /classify        — Single feedback text → structured result
POST /classify/bulk   — CSV file → array of results
GET  /results         — Paginated results with filters (sentiment, date, priority)
```

### Environment Variables

```
OPENAI_API_KEY
CHAT_MODEL=gpt-4o-mini
DB_PATH=./data/feedback.db
```

### Extension Ideas
- Add topic clustering with embeddings to group similar complaints automatically
- Integrate with a webhook to receive live support ticket events
- Build a trend chart showing sentiment shift over time
