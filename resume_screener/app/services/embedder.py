from __future__ import annotations

import numpy as np
from openai import OpenAI

from app.core.config import Settings


class EmbeddingService:
    """Handles text embedding and vector similarity (SRP)."""

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.embedding_model

    def get_embedding(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            input=text,
            model=self._model,
        )
        return response.data[0].embedding

    @staticmethod
    def compute_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
        a = np.array(embedding_a)
        b = np.array(embedding_b)
        dot = np.dot(a, b)
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        if norm == 0:
            return 0.0
        return float(dot / norm)
