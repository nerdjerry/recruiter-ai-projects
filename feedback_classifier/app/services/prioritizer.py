"""Priority scoring service (SRP — only computes priority)."""

from __future__ import annotations

from datetime import datetime


class PriorityService:
    """Scores feedback items by severity × recency."""

    @staticmethod
    def compute_priority(severity: int, submitted_at: datetime) -> float:
        """Return priority score.

        Formula: severity * recency_weight
        recency_weight decays linearly from 1.0 (today) to 0.5 (30+ days).
        """
        age_days = (datetime.utcnow() - submitted_at).total_seconds() / 86400
        recency_weight = max(1.0 - (age_days / 60), 0.5)
        return round(severity * recency_weight, 2)
