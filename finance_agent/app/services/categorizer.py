from __future__ import annotations

import openai

from app.core.config import Settings
from app.core.prompts import CATEGORIZE_PROMPT


class CategorizationService:
    """LLM-based transaction categorization."""

    VALID_CATEGORIES = {
        "food", "transport", "entertainment", "bills",
        "shopping", "health", "other",
    }

    def __init__(self, config: Settings) -> None:
        self._client = openai.OpenAI(api_key=config.openai_api_key)
        self._model = config.chat_model

    def categorize(self, description: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "user", "content": CATEGORIZE_PROMPT.format(description=description)},
                ],
                max_tokens=10,
                temperature=0,
            )
            category = response.choices[0].message.content.strip().lower()
            return category if category in self.VALID_CATEGORIES else "other"
        except Exception:
            return "other"
