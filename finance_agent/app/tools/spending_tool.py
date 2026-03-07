from __future__ import annotations

from collections import defaultdict

from app.services.plaid_client import BaseTransactionSource


class SpendingTool:
    """Queries and aggregates transaction data (SRP)."""

    def __init__(self, transaction_source: BaseTransactionSource) -> None:
        self._source = transaction_source

    def run(self, days: int = 30, category: str | None = None) -> str:
        transactions = self._source.fetch(days=days)
        if category:
            transactions = [t for t in transactions if t.category == category]
        if not transactions:
            return f"No transactions found in the last {days} days."

        total = sum(t.amount for t in transactions)
        by_category: dict[str, float] = defaultdict(float)
        for t in transactions:
            by_category[t.category] += t.amount

        lines = [f"Spending summary (last {days} days):"]
        lines.append(f"  Total: ${total:,.2f}")
        lines.append(f"  Transactions: {len(transactions)}")
        lines.append("  By category:")
        for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
            lines.append(f"    {cat}: ${amt:,.2f}")
        return "\n".join(lines)
