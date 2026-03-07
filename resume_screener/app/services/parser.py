from __future__ import annotations

import io
from abc import ABC, abstractmethod
from pathlib import Path

import docx
from PyPDF2 import PdfReader


class BaseParser(ABC):
    """Abstract base class for resume parsers."""

    @abstractmethod
    def parse(self, file_bytes: bytes, filename: str) -> str:
        """Extract plain text from file bytes."""


class PdfParser(BaseParser):
    def parse(self, file_bytes: bytes, filename: str) -> str:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()


class DocxParser(BaseParser):
    def parse(self, file_bytes: bytes, filename: str) -> str:
        document = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in document.paragraphs]
        return "\n".join(paragraphs).strip()


class ParserFactory:
    """Picks the correct parser based on file extension (Open/Closed)."""

    _parsers: dict[str, type[BaseParser]] = {
        ".pdf": PdfParser,
        ".docx": DocxParser,
    }

    @classmethod
    def register(cls, extension: str, parser_cls: type[BaseParser]) -> None:
        ext = extension if extension.startswith(".") else f".{extension}"
        cls._parsers[ext.lower()] = parser_cls

    @classmethod
    def get_parser(cls, filename: str) -> BaseParser:
        ext = Path(filename).suffix.lower()
        parser_cls = cls._parsers.get(ext)
        if parser_cls is None:
            raise ValueError(f"Unsupported file type: {ext}")
        return parser_cls()
