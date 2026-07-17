"""
snapshot.py

Domain model representing a financial snapshot.

Responsibilities:
- Store point-in-time financial metrics.
- Used for historical tracking.
- No calculations or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Snapshot:
    id: str = field(default_factory=lambda: str(uuid4()))

    snapshot_date: datetime = field(default_factory=datetime.now)

    net_worth: float = 0.0

    total_assets: float = 0.0
    total_liabilities: float = 0.0

    total_cash: float = 0.0

    total_investments: float = 0.0

    total_income: float = 0.0
    total_expenses: float = 0.0

    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        numeric_fields = [
            self.net_worth,
            self.total_assets,
            self.total_liabilities,
            self.total_cash,
            self.total_investments,
            self.total_income,
            self.total_expenses,
        ]

        if any(value < 0 for value in numeric_fields):
            raise ValueError("Snapshot values cannot be negative.")

    def to_dict(self) -> dict:
        data = asdict(self)
        data["snapshot_date"] = self.snapshot_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Snapshot":
        return cls(
            id=data["id"],
            snapshot_date=datetime.fromisoformat(data["snapshot_date"]),
            net_worth=data.get("net_worth", 0.0),
            total_assets=data.get("total_assets", 0.0),
            total_liabilities=data.get("total_liabilities", 0.0),
            total_cash=data.get("total_cash", 0.0),
            total_investments=data.get("total_investments", 0.0),
            total_income=data.get("total_income", 0.0),
            total_expenses=data.get("total_expenses", 0.0),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )