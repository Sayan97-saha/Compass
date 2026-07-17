"""
reminder.py

Domain model representing a reminder.

Responsibilities:
- Store reminder information.
- Track reminder schedule and status.
- No notification or scheduling logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class ReminderType(Enum):
    BILL = "BILL"
    EMI = "EMI"
    SIP = "SIP"
    INSURANCE = "INSURANCE"
    CREDIT_CARD = "CREDIT_CARD"
    SUBSCRIPTION = "SUBSCRIPTION"
    INVESTMENT = "INVESTMENT"
    OTHER = "OTHER"


class ReminderStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Reminder:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    reminder_type: ReminderType = ReminderType.OTHER

    due_date: date = field(default_factory=date.today)
    amount: Optional[float] = None

    account_id: Optional[str] = None
    category_id: Optional[str] = None

    status: ReminderStatus = ReminderStatus.ACTIVE

    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Reminder title cannot be empty.")

        if not isinstance(self.reminder_type, ReminderType):
            raise ValueError("Invalid reminder type.")

        if not isinstance(self.status, ReminderStatus):
            raise ValueError("Invalid reminder status.")

        if self.amount is not None and self.amount < 0:
            raise ValueError("Amount cannot be negative.")

    def mark_completed(self) -> None:
        self.status = ReminderStatus.COMPLETED
        self.updated_at = datetime.now()

    def cancel(self) -> None:
        self.status = ReminderStatus.CANCELLED
        self.updated_at = datetime.now()

    def rename(self, title: str) -> None:
        self.title = title
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
        data["reminder_type"] = self.reminder_type.value
        data["status"] = self.status.value
        data["due_date"] = self.due_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Reminder":
        return cls(
            id=data["id"],
            title=data["title"],
            reminder_type=ReminderType(data["reminder_type"]),
            due_date=date.fromisoformat(data["due_date"]),
            amount=data.get("amount"),
            account_id=data.get("account_id"),
            category_id=data.get("category_id"),
            status=ReminderStatus(data["status"]),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )