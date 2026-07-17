"""
transaction.py

Domain model representing a financial transaction.

Responsibilities:
- Represent a single financial event.
- Validate transaction data.
- No balance calculations.
- No persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"


class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Transaction:
    id: str = field(default_factory=lambda: str(uuid4()))

    account_id: str = ""
    category_id: str = ""
    merchant_id: Optional[str] = None

    transaction_type: TransactionType = TransactionType.EXPENSE
    status: TransactionStatus = TransactionStatus.COMPLETED

    amount: float = 0.0
    transaction_date: datetime = field(default_factory=datetime.now)

    description: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.account_id.strip():
            raise ValueError("Account ID cannot be empty.")

        if not self.category_id.strip():
            raise ValueError("Category ID cannot be empty.")

        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if not isinstance(self.transaction_type, TransactionType):
            raise ValueError("Invalid transaction type.")

        if not isinstance(self.status, TransactionStatus):
            raise ValueError("Invalid transaction status.")

    def update_status(self, status: TransactionStatus) -> None:
        self.status = status
        self.updated_at = datetime.now()

    def update_notes(self, notes: str) -> None:
        self.notes = notes
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["transaction_type"] = self.transaction_type.value
        data["status"] = self.status.value
        data["transaction_date"] = self.transaction_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            id=data["id"],
            account_id=data["account_id"],
            category_id=data["category_id"],
            merchant_id=data.get("merchant_id"),
            transaction_type=TransactionType(data["transaction_type"]),
            status=TransactionStatus(data["status"]),
            amount=data["amount"],
            transaction_date=datetime.fromisoformat(data["transaction_date"]),
            description=data.get("description"),
            reference_number=data.get("reference_number"),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )