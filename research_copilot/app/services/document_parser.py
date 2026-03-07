"""Document text extraction service (SRP — thin routers)."""

from __future__ import annotations

import io

from PyPDF2 import PdfReader


def extract_text(raw: bytes, filename: str) -> str:
    """Extract plain text from raw file bytes based on filename extension."""
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return raw.decode("utf-8", errors="ignore")
