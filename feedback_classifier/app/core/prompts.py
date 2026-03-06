"""Prompt templates stored as constants (never inline)."""

CLASSIFICATION_PROMPT = """\
You are a customer feedback classifier. Analyze the feedback text below and \
return a JSON object with exactly these fields:

- "sentiment": one of "positive", "neutral", or "negative"
- "topic": a short category label (e.g. "billing", "UI/UX", "performance")
- "summary": a one-sentence summary of the feedback
- "severity": an integer from 1 (trivial) to 5 (critical)

Return ONLY valid JSON, no markdown fences, no extra text.

Feedback:
{text}
"""
