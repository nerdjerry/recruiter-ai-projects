"""Prompt templates for LLM calls."""

CLASSIFY_PROMPT = """\
You are an email classification assistant. Analyse the email below and return
a JSON object with exactly three keys:

- "intent": one of "inquiry", "complaint", "scheduling", "spam", "other"
- "urgency": one of "high", "medium", "low"
- "confidence": a float between 0 and 1

Subject: {subject}

Body:
{body}

Respond ONLY with valid JSON, no markdown fences or extra text.
"""

DRAFT_REPLY_PROMPT = """\
You are a professional email assistant. Draft a concise, polite reply to the
email below.  The email has been classified as:

Intent: {intent}
Urgency: {urgency}

Original subject: {subject}
Original body:
{body}

Return ONLY a JSON object with exactly three keys:
- "subject": the reply subject line
- "body": the reply body text
- "tone": one of "formal", "friendly", "empathetic", "neutral"

Respond ONLY with valid JSON, no markdown fences or extra text.
"""
