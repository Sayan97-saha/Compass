"""
asset.py

Domain model representing an asset.

Responsibilities:
- Store information about assets.
- Track current valuation.
- No valuation or investment logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class AssetType(Enum):
    CASH = "CASH"
    PROPERTY = "PROPERTY"
    VEHICLE = "VEHICLE"
    GOLD = "GOLD"
    SILVER = "SILVER"
    STOCK = "STOCK"
    MUTUAL_FUND = "MUTUAL_FUND"
    CRYPTO = "CRYPTO"
    BOND = "BOND"
    PPF = "PPF"
    EPF = "EPF"
    NPS = "NPS"
    FD = "FD"
    RD = "RD"
    OTHER = "OTHER"


@dataclass
class Asset:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    asset_type: AssetType = AssetType.OTHER
    institution_id: Optional[str] = None

    purchase_date: Optional[datetime] = None
    purchase_value: float = 0.0
    current_value: float = 0.0

    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Asset name cannot be empty.")

        if not isinstance(self.asset_type, AssetType):
            raise ValueError("Invalid asset type.")

        if self.purchase_value < 0:
            raise ValueError("Purchase value cannot be negative.")

        if self.current_value < 0:
            raise ValueError("Current value cannot be negative.")

    def update_value(self, value: float) -> None:
        if value < 0:
            raise ValueError("Current value cannot be negative.")
        self.current_value = value
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
        data["asset_type"] = self.asset_type.value
        data["purchase_date"] = (
            self.purchase_date.isoformat() if self.purchase_date else None
        )
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Asset":
        return cls(
            id=data["id"],
            name=data["name"],
            asset_type=AssetType(data["asset_type"]),
            institution_id=data.get("institution_id"),
            purchase_date=(
                datetime.fromisoformat(data["purchase_date"])
                if data.get("purchase_date")
                else None
            ),
            purchase_value=data.get("purchase_value", 0.0),
            current_value=data.get("current_value", 0.0),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )