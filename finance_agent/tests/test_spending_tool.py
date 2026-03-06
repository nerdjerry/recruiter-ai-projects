from datetime import date

from app.models.schemas import Transaction
from app.services.plaid_client import BaseTransactionSource
from app.tools.spending_tool import SpendingTool


class MockTransactionSource(BaseTransactionSource):
    def __init__(self, transactions: list[Transaction]) -> None:
        self._transactions = transactions

    def fetch(self, days: int = 30) -> list[Transaction]:
        return self._transactions


SAMPLE_TRANSACTIONS = [
    Transaction(id="1", date=date.today(), description="Grocery Store", amount=50.0, category="food", source="csv"),
    Transaction(id="2", date=date.today(), description="Gas Station", amount=40.0, category="transport", source="csv"),
    Transaction(id="3", date=date.today(), description="Restaurant", amount=30.0, category="food", source="csv"),
    Transaction(id="4", date=date.today(), description="Netflix", amount=15.0, category="entertainment", source="csv"),
]


class TestSpendingTool:
    def test_summary_output(self):
        source = MockTransactionSource(SAMPLE_TRANSACTIONS)
        tool = SpendingTool(transaction_source=source)
        result = tool.run(days=30)
        assert "135.00" in result
        assert "food" in result
        assert "transport" in result

    def test_category_filter(self):
        source = MockTransactionSource(SAMPLE_TRANSACTIONS)
        tool = SpendingTool(transaction_source=source)
        result = tool.run(days=30, category="food")
        assert "80.00" in result
        assert "transport" not in result

    def test_no_transactions(self):
        source = MockTransactionSource([])
        tool = SpendingTool(transaction_source=source)
        result = tool.run(days=30)
        assert "No transactions" in result
