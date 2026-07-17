"""
investment.py

Domain model representing an investment holding.

Responsibilities:
- Store investment holding information.
- Track quantity and valuation.
- No portfolio calculations or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class InvestmentType(Enum):
    STOCK = "STOCK"
    MUTUAL_FUND = "MUTUAL_FUND"
    ETF = "ETF"
    BOND = "BOND"
    GOLD = "GOLD"
    SILVER = "SILVER"
    CRYPTO = "CRYPTO"
    NPS = "NPS"
    PPF = "PPF"
    EPF = "EPF"
    FD = "FD"
    RD = "RD"
    OTHER = "OTHER"


@dataclass
class Investment:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    investment_type: InvestmentType = InvestmentType.OTHER
    institution_id: Optional[str] = None

    symbol: Optional[str] = None

    quantity: float = 0.0
    average_buy_price: float = 0.0
    current_price: float = 0.0

    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Investment name cannot be empty.")

        if not isinstance(self.investment_type, InvestmentType):
            raise ValueError("Invalid investment type.")

        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if self.average_buy_price < 0:
            raise ValueError("Average buy price cannot be negative.")

        if self.current_price < 0:
            raise ValueError("Current price cannot be negative.")

    @property
    def invested_value(self) -> float:
        return self.quantity * self.average_buy_price

    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def profit_loss(self) -> float:
        return self.current_value - self.invested_value

    def update_price(self, price: float) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.current_price = price
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
        data["investment_type"] = self.investment_type.value
        data["purchase_date"] = (
            self.purchase_date.isoformat() if self.purchase_date else None
        )
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Investment":
        return cls(
            id=data["id"],
            name=data["name"],
            investment_type=InvestmentType(data["investment_type"]),
            institution_id=data.get("institution_id"),
            symbol=data.get("symbol"),
            quantity=data.get("quantity", 0.0),
            average_buy_price=data.get("average_buy_price", 0.0),
            current_price=data.get("current_price", 0.0),
            purchase_date=(
                datetime.fromisoformat(data["purchase_date"])
                if data.get("purchase_date")
                else None
            ),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )