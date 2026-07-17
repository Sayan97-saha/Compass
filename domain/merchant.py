"""
merchant.py

Domain model representing a transaction merchant/payee.

Responsibilities:
- Store merchant information.
- Used by transactions for reporting and analysis.
- No transaction or persistence logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Merchant:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    category_id: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Merchant name cannot be empty.")

    def rename(self, new_name: str) -> None:
        self.name = new_name
        self.updated_at = datetime.now()
        self.validate()

    def update_category(self, category_id: Optional[str]) -> None:
        self.category_id = category_id
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Merchant":
        return cls(
            id=data["id"],
            name=data["name"],
            category_id=data.get("category_id"),
            website=data.get("website"),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )