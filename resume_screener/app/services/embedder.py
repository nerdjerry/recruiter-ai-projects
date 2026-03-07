from __future__ import annotations

import numpy as np
from langchain_openai import OpenAIEmbeddings

from app.core.config import Settings


class EmbeddingService:
    """Handles text embedding and vector similarity using LangChain (SRP)."""

    def __init__(self, settings: Settings) -> None:
        self._embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )

    def get_embedding(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)

    async def aget_embedding(self, text: str) -> list[float]:
        return await self._embeddings.aembed_query(text)

    @staticmethod
    def compute_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
        a = np.array(embedding_a)
        b = np.array(embedding_b)
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        if norm == 0:
            return 0.0
        return float(dot / norm)
