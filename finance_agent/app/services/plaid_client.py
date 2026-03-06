from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.schemas import Transaction


class BaseTransactionSource(ABC):
    @abstractmethod
    def fetch(self, days: int = 30) -> list[Transaction]: ...


class PlaidClient(BaseTransactionSource):
    """Plaid sandbox client — requires valid credentials to function."""

    def __init__(self, client_id: str, secret: str, env: str = "sandbox") -> None:
        self._client_id = client_id
        self._secret = secret
        self._env = env

    def fetch(self, days: int = 30) -> list[Transaction]:
        raise NotImplementedError(
            "Plaid integration requires valid credentials. "
            "Set PLAID_CLIENT_ID and PLAID_SECRET in your .env file, "
            "or use the CSV importer as a fallback."
        )
