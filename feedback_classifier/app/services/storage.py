"""SQLite persistence service (SRP — only manages DB read/write)."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime

from app.models.schemas import FeedbackOut, PaginatedResults

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS feedback (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    text          TEXT    NOT NULL,
    sentiment     TEXT    NOT NULL,
    topic         TEXT    NOT NULL,
    summary       TEXT    NOT NULL,
    severity      INTEGER NOT NULL,
    priority_score REAL   NOT NULL,
    source        TEXT    NOT NULL,
    submitted_at  TEXT    NOT NULL,
    classified_at TEXT    NOT NULL
);
"""


class StorageService:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def init_db(self) -> None:
        os.makedirs(os.path.dirname(self._db_path) or ".", exist_ok=True)
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)

    def save(self, feedback: FeedbackOut) -> FeedbackOut:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO feedback "
                "(text,sentiment,topic,summary,severity,"
                "priority_score,source,submitted_at,classified_at) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    feedback.text,
                    feedback.sentiment,
                    feedback.topic,
                    feedback.summary,
                    feedback.severity,
                    feedback.priority_score,
                    feedback.source,
                    feedback.submitted_at.isoformat(),
                    feedback.classified_at.isoformat(),
                ),
            )
            return feedback.model_copy(update={"id": cursor.lastrowid})

    def get_results(
        self,
        page: int = 1,
        page_size: int = 20,
        sentiment_filter: str | None = None,
        min_priority: float | None = None,
    ) -> PaginatedResults:
        clauses: list[str] = []
        params: list[object] = []
        if sentiment_filter:
            clauses.append("sentiment = ?")
            params.append(sentiment_filter)
        if min_priority is not None:
            clauses.append("priority_score >= ?")
            params.append(min_priority)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as conn:
            total = conn.execute(
                f"SELECT COUNT(*) FROM feedback {where}", params
            ).fetchone()[0]
            rows = conn.execute(
                f"SELECT * FROM feedback {where} "
                f"ORDER BY id DESC LIMIT ? OFFSET ?",
                [*params, page_size, (page - 1) * page_size],
            ).fetchall()

        items = [self._row_to_feedback(r) for r in rows]
        return PaginatedResults(
            items=items, total=total, page=page, page_size=page_size
        )

    # ------------------------------------------------------------------
    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    @staticmethod
    def _row_to_feedback(row: tuple) -> FeedbackOut:
        return FeedbackOut(
            id=row[0],
            text=row[1],
            sentiment=row[2],
            topic=row[3],
            summary=row[4],
            severity=row[5],
            priority_score=row[6],
            source=row[7],
            submitted_at=datetime.fromisoformat(row[8]),
            classified_at=datetime.fromisoformat(row[9]),
        )
