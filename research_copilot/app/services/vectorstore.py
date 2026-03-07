"""Document ingestion and FAISS-based vector store with persistence via LangChain."""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

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
    """FAISS-backed vector store with persistence via LangChain."""

    def __init__(
        self, embedding_model: str, vectorstore_path: str, openai_api_key: str
    ) -> None:
        self._embedding_model = embedding_model
        self._vectorstore_path = vectorstore_path
        self._embeddings = OpenAIEmbeddings(
            model=embedding_model, api_key=openai_api_key
        )
        self._documents: list[DocumentInfo] = []
        self._faiss: FAISS | None = None
        self._load()

    def _load(self) -> None:
        """Load persisted FAISS index from disk if it exists."""
        if os.path.exists(self._vectorstore_path):
            try:
                self._faiss = FAISS.load_local(
                    self._vectorstore_path,
                    self._embeddings,
                    allow_dangerous_deserialization=True,
                )
            except Exception:
                self._faiss = None

    def _save(self) -> None:
        """Persist FAISS index to disk."""
        if self._faiss is not None:
            os.makedirs(os.path.dirname(self._vectorstore_path) or ".", exist_ok=True)
            self._faiss.save_local(self._vectorstore_path)

    def add_document(self, filename: str, text: str) -> DocumentInfo:
        doc_id = uuid.uuid4().hex[:12]
        chunks = _chunk_text(text)
        metadatas = [{"doc_id": doc_id} for _ in chunks]

        if self._faiss is None:
            self._faiss = FAISS.from_texts(chunks, self._embeddings, metadatas=metadatas)
        else:
            self._faiss.add_texts(chunks, metadatas=metadatas)

        self._save()

        info = DocumentInfo(
            id=doc_id,
            filename=filename,
            chunk_count=len(chunks),
            uploaded_at=datetime.now(timezone.utc),
        )
        self._documents.append(info)
        return info

    def search(self, query: str, top_k: int = 3) -> list[ToolResult]:
        if self._faiss is None:
            return []
        results = self._faiss.similarity_search(query, k=top_k)
        return [
            ToolResult(
                content=doc.page_content,
                source_name="knowledge_base",
                doc_id=doc.metadata.get("doc_id"),
            )
            for doc in results
        ]

    def list_documents(self) -> list[DocumentInfo]:
        return list(self._documents)
