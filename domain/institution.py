"""
institution.py

Domain model representing a financial institution.

Responsibilities:
- Store institution information.
- Own one or more financial accounts.
- No business logic related to balances, transactions, or persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class InstitutionType(Enum):
    BANK = "BANK"
    BROKER = "BROKER"
    INSURANCE = "INSURANCE"
    EPF = "EPF"
    CREDIT_CARD = "CREDIT_CARD"
    NBFC = "NBFC"
    OTHER = "OTHER"


@dataclass
class Institution:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    institution_type: InstitutionType = InstitutionType.OTHER
    short_name: Optional[str] = None
    website: Optional[str] = None
    customer_care: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate institution data."""

        if not self.name.strip():
            raise ValueError("Institution name cannot be empty.")

        if not isinstance(self.institution_type, InstitutionType):
            raise ValueError("Invalid institution type.")

    def update_details(
        self,
        *,
        name: Optional[str] = None,
        short_name: Optional[str] = None,
        institution_type: Optional[InstitutionType] = None,
        website: Optional[str] = None,
        customer_care: Optional[str] = None,
    ) -> None:
        """Update institution details."""

        if name is not None:
            self.name = name

        if short_name is not None:
            self.short_name = short_name

        if institution_type is not None:
            self.institution_type = institution_type

        if website is not None:
            self.website = website

        if customer_care is not None:
            self.customer_care = customer_care

        self.updated_at = datetime.now()
        self.validate()

    def activate(self) -> None:
        """Mark institution as active."""
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        """Mark institution as inactive."""
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert object to dictionary."""
        data = asdict(self)
        data["institution_type"] = self.institution_type.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Institution":
        """Create Institution from dictionary."""

        return cls(
            id=data["id"],
            name=data["name"],
            institution_type=InstitutionType(data["institution_type"]),
            short_name=data.get("short_name"),
            website=data.get("website"),
            customer_care=data.get("customer_care"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )