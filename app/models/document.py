from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class Document(SQLModel, table=True):

    __tablename__ = "documents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    invoice_id: UUID = Field(
        foreign_key="invoices.id_invoice",
        nullable=False,
        unique=True
    )

    file_url: str = Field(nullable=False)
    file_type: Optional[str] = Field(default=None, max_length=20)

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    invoice: Optional["Invoice"] = Relationship(back_populates="document") # type: ignore