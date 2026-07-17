"""
document.py

Domain model representing a financial document.

Responsibilities:
- Store metadata for financial documents.
- Link documents to domain entities.
- No file storage or OCR logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class DocumentType(Enum):
    INVOICE = "INVOICE"
    RECEIPT = "RECEIPT"
    BANK_STATEMENT = "BANK_STATEMENT"
    CREDIT_CARD_STATEMENT = "CREDIT_CARD_STATEMENT"
    INSURANCE = "INSURANCE"
    TAX = "TAX"
    INVESTMENT = "INVESTMENT"
    LOAN = "LOAN"
    OTHER = "OTHER"


@dataclass
class Document:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    document_type: DocumentType = DocumentType.OTHER

    file_name: str = ""
    file_path: str = ""
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

    linked_entity: Optional[str] = None
    linked_entity_id: Optional[str] = None

    notes: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    is_active: bool = True

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Document title cannot be empty.")

        if not self.file_name.strip():
            raise ValueError("File name cannot be empty.")

        if not self.file_path.strip():
            raise ValueError("File path cannot be empty.")

        if not isinstance(self.document_type, DocumentType):
            raise ValueError("Invalid document type.")

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
        data["document_type"] = self.document_type.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        return cls(
            id=data["id"],
            title=data["title"],
            document_type=DocumentType(data["document_type"]),
            file_name=data["file_name"],
            file_path=data["file_path"],
            file_size=data.get("file_size"),
            mime_type=data.get("mime_type"),
            linked_entity=data.get("linked_entity"),
            linked_entity_id=data.get("linked_entity_id"),
            notes=data.get("notes"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            is_active=data.get("is_active", True),
        )