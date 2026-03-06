from __future__ import annotations

import csv
import io
import os
import sqlite3
import uuid
from datetime import date, timedelta

from app.models.schemas import Transaction
from app.services.plaid_client import BaseTransactionSource


class CsvImporter(BaseTransactionSource):
    """CSV-based transaction source backed by SQLite."""

    def __init__(self, db_path: str = "./data/transactions.db") -> None:
        self._db_path = db_path
        self.init_db()

    def init_db(self) -> None:
        os.makedirs(os.path.dirname(self._db_path) or ".", exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT DEFAULT 'other',
                    source TEXT DEFAULT 'csv'
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def import_csv(self, file_content: str) -> list[Transaction]:
        reader = csv.DictReader(io.StringIO(file_content))
        transactions: list[Transaction] = []
        for row in reader:
            txn = Transaction(
                id=str(uuid.uuid4()),
                date=date.fromisoformat(row["date"]),
                description=row["description"],
                amount=float(row["amount"]),
                category=row.get("category", "other"),
                source="csv",
            )
            transactions.append(txn)
        return transactions

    def save_transactions(self, transactions: list[Transaction]) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO transactions VALUES (?,?,?,?,?,?)",
                [(t.id, t.date.isoformat(), t.description, t.amount, t.category, t.source) for t in transactions],
            )

    def fetch(self, days: int = 30) -> list[Transaction]:
        return self.get_transactions(days=days)

    def get_transactions(
        self,
        days: int | None = None,
        category: str | None = None,
        min_amount: float | None = None,
    ) -> list[Transaction]:
        query = "SELECT id, date, description, amount, category, source FROM transactions WHERE 1=1"
        params: list = []
        if days:
            cutoff = (date.today() - timedelta(days=days)).isoformat()
            query += " AND date >= ?"
            params.append(cutoff)
        if category:
            query += " AND category = ?"
            params.append(category)
        if min_amount is not None:
            query += " AND amount >= ?"
            params.append(min_amount)
        query += " ORDER BY date DESC"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [
            Transaction(id=r[0], date=date.fromisoformat(r[1]), description=r[2], amount=r[3], category=r[4], source=r[5])
            for r in rows
        ]
