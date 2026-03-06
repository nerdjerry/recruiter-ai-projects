"""Exporters — Open/Closed + Liskov Substitution via BaseExporter."""

from __future__ import annotations

import csv
import io
import json
from abc import ABC, abstractmethod

from app.models.schemas import FeedbackOut


class BaseExporter(ABC):
    """Abstract base; any new format extends without modifying existing code."""

    @abstractmethod
    def export(self, results: list[FeedbackOut]) -> str:
        ...


class JsonExporter(BaseExporter):
    def export(self, results: list[FeedbackOut]) -> str:
        return json.dumps(
            [r.model_dump(mode="json") for r in results], indent=2
        )


class CsvExporter(BaseExporter):
    def export(self, results: list[FeedbackOut]) -> str:
        if not results:
            return ""
        buf = io.StringIO()
        fields = list(results[0].model_fields.keys())
        writer = csv.DictWriter(buf, fieldnames=fields)
        writer.writeheader()
        for r in results:
            writer.writerow(r.model_dump(mode="json"))
        return buf.getvalue()


class MarkdownExporter(BaseExporter):
    def export(self, results: list[FeedbackOut]) -> str:
        if not results:
            return ""
        fields = list(results[0].model_fields.keys())
        lines = [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
        ]
        for r in results:
            vals = r.model_dump(mode="json")
            lines.append("| " + " | ".join(str(vals[f]) for f in fields) + " |")
        return "\n".join(lines)
