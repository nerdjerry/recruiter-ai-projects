from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.prompts import CATEGORIZE_PROMPT


class CategorizationService:
    """LLM-based transaction categorization via LangChain."""

    VALID_CATEGORIES = {
        "food", "transport", "entertainment", "bills",
        "shopping", "health", "other",
    }

    def __init__(self, config: Settings) -> None:
        self._llm = ChatOpenAI(
            model=config.chat_model,
            api_key=config.openai_api_key,
            max_tokens=10,
            temperature=0,
        )

    def categorize(self, description: str) -> str:
        try:
            response = self._llm.invoke([
                ("human", CATEGORIZE_PROMPT.format(description=description)),
            ])
            category = response.content.strip().lower()
            return category if category in self.VALID_CATEGORIES else "other"
        except Exception:
            return "other"
