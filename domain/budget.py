"""
budget.py

Domain model representing a budget.

Responsibilities:
- Store budget configuration.
- Track spending limits.
- No calculations or reporting logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class BudgetPeriod(Enum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"


@dataclass
class Budget:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    category_id: str = ""

    amount: float = 0.0
    period: BudgetPeriod = BudgetPeriod.MONTHLY

    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None

    rollover: bool = False

    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Budget name cannot be empty.")

        if not self.category_id.strip():
            raise ValueError("Category ID cannot be empty.")

        if self.amount <= 0:
            raise ValueError("Budget amount must be greater than zero.")

        if not isinstance(self.period, BudgetPeriod):
            raise ValueError("Invalid budget period.")

    def update_amount(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Budget amount must be greater than zero.")

        self.amount = amount
        self.updated_at = datetime.now()

    def rename(self, name: str) -> None:
        self.name = name
        self.updated_at = datetime.now()
        self.validate()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["period"] = self.period.value
        data["start_date"] = self.start_date.isoformat()
        data["end_date"] = (
            self.end_date.isoformat() if self.end_date else None
        )
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        return cls(
            id=data["id"],
            name=data["name"],
            category_id=data["category_id"],
            amount=data["amount"],
            period=BudgetPeriod(data["period"]),
            start_date=date.fromisoformat(data["start_date"]),
            end_date=(
                date.fromisoformat(data["end_date"])
                if data.get("end_date")
                else None
            ),
            rollover=data.get("rollover", False),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )