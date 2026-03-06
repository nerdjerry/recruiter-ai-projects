"""Document ingestion and numpy-based vector store (no FAISS required)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import numpy as np
import openai

from app.models.schemas import DocumentInfo, ToolResult


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks or [text]


class VectorStoreService:
    """In-memory vector store using numpy cosine similarity."""

    def __init__(
        self, embedding_model: str, vectorstore_path: str, openai_api_key: str
    ) -> None:
        self._embedding_model = embedding_model
        self._vectorstore_path = vectorstore_path
        self._client = openai.OpenAI(api_key=openai_api_key)
        self._documents: list[DocumentInfo] = []
        self._chunks: list[dict] = []  # {text, doc_id, embedding}

    def _embed(self, texts: list[str]) -> np.ndarray:
        resp = self._client.embeddings.create(model=self._embedding_model, input=texts)
        return np.array([d.embedding for d in resp.data])

    def add_document(self, filename: str, text: str) -> DocumentInfo:
        doc_id = uuid.uuid4().hex[:12]
        chunks = _chunk_text(text)
        embeddings = self._embed(chunks)
        for i, chunk in enumerate(chunks):
            self._chunks.append(
                {"text": chunk, "doc_id": doc_id, "embedding": embeddings[i]}
            )
        info = DocumentInfo(
            id=doc_id,
            filename=filename,
            chunk_count=len(chunks),
            uploaded_at=datetime.now(timezone.utc),
        )
        self._documents.append(info)
        return info

    def search(self, query: str, top_k: int = 3) -> list[ToolResult]:
        if not self._chunks:
            return []
        q_emb = self._embed([query])[0]
        scores: list[tuple[float, int]] = []
        for idx, chunk in enumerate(self._chunks):
            emb = chunk["embedding"]
            cos = float(np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb) + 1e-10))
            scores.append((cos, idx))
        scores.sort(key=lambda x: x[0], reverse=True)
        results: list[ToolResult] = []
        for score, idx in scores[:top_k]:
            c = self._chunks[idx]
            results.append(
                ToolResult(content=c["text"], source_name="knowledge_base")
            )
        return results

    def list_documents(self) -> list[DocumentInfo]:
        return list(self._documents)
