"""
category.py

Domain model representing a transaction category.

Responsibilities:
- Classify transactions.
- Support parent-child hierarchy.
- No budgeting or reporting logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class CategoryType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"


@dataclass
class Category:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    category_type: CategoryType = CategoryType.EXPENSE
    parent_category_id: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("Category name cannot be empty.")

        if not isinstance(self.category_type, CategoryType):
            raise ValueError("Invalid category type.")

    def rename(self, new_name: str) -> None:
        self.name = new_name
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
        data["category_type"] = self.category_type.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(
            id=data["id"],
            name=data["name"],
            category_type=CategoryType(data["category_type"]),
            parent_category_id=data.get("parent_category_id"),
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )