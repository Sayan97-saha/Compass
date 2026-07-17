"""
goal.py

Domain model representing a financial goal.

Responsibilities:
- Store financial goal information.
- Track target and current progress.
- No forecasting or contribution calculations.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class GoalStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Goal:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    target_amount: float = 0.0
    current_amount: float = 0.0
    target_date: Optional[date] = None
    status: GoalStatus = GoalStatus.ACTIVE
    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Goal name cannot be empty.")

        if self.target_amount <= 0:
            raise ValueError("Target amount must be greater than zero.")

        if self.current_amount < 0:
            raise ValueError("Current amount cannot be negative.")

        if not isinstance(self.status, GoalStatus):
            raise ValueError("Invalid goal status.")

    @property
    def progress_percentage(self) -> float:
        return round((self.current_amount / self.target_amount) * 100, 2)

    def update_progress(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Current amount cannot be negative.")

        self.current_amount = amount
        self.updated_at = datetime.now()

    def rename(self, name: str) -> None:
        self.name = name
        self.updated_at = datetime.now()
        self.validate()

    def mark_completed(self) -> None:
        self.status = GoalStatus.COMPLETED
        self.updated_at = datetime.now()

    def cancel(self) -> None:
        self.status = GoalStatus.CANCELLED
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        data["target_date"] = (
            self.target_date.isoformat() if self.target_date else None
        )
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Goal":
        return cls(
            id=data["id"],
            name=data["name"],
            target_amount=data["target_amount"],
            current_amount=data.get("current_amount", 0.0),
            target_date=(
                date.fromisoformat(data["target_date"])
                if data.get("target_date")
                else None
            ),
            status=GoalStatus(data["status"]),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )