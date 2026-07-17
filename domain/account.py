"""
account.py

Domain model representing a financial account.

Responsibilities:
- Store account information.
- Belong to exactly one Institution.
- Maintain current balance.
- No transaction logic or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class AccountType(Enum):
    SAVINGS = "SAVINGS"
    CURRENT = "CURRENT"
    CREDIT_CARD = "CREDIT_CARD"
    CASH = "CASH"
    LOAN = "LOAN"
    PPF = "PPF"
    EPF = "EPF"
    FD = "FD"
    RD = "RD"
    DEMAT = "DEMAT"
    MUTUAL_FUND = "MUTUAL_FUND"
    WALLET = "WALLET"
    OTHER = "OTHER"


@dataclass
class Account:
    id: str = field(default_factory=lambda: str(uuid4()))
    institution_id: str = ""
    name: str = ""
    account_type: AccountType = AccountType.OTHER
    account_number: Optional[str] = None
    currency: str = "INR"
    opening_balance: float = 0.0
    current_balance: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.institution_id.strip():
            raise ValueError("Institution ID cannot be empty.")

        if not self.name.strip():
            raise ValueError("Account name cannot be empty.")

        if not isinstance(self.account_type, AccountType):
            raise ValueError("Invalid account type.")

    def rename(self, new_name: str) -> None:
        self.name = new_name
        self.updated_at = datetime.now()
        self.validate()

    def update_balance(self, balance: float) -> None:
        self.current_balance = balance
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["account_type"] = self.account_type.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(
            id=data["id"],
            institution_id=data["institution_id"],
            name=data["name"],
            account_type=AccountType(data["account_type"]),
            account_number=data.get("account_number"),
            currency=data.get("currency", "INR"),
            opening_balance=data.get("opening_balance", 0.0),
            current_balance=data.get("current_balance", 0.0),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )