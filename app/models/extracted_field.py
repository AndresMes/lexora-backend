from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class ExtractedField(SQLModel, table=True):
    __tablename__ = "extracted_fields"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    invoice_id: UUID = Field(foreign_key="invoices.id", nullable=False)

    field_name: str = Field(nullable=False, max_length=100)
    extracted_value: Optional[str] = None
    confidence: Optional[float] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    invoice: Optional["Invoice"] = Relationship(back_populates="extracted_fields") #type: ignore
    corrections: list["FieldCorrection"] = Relationship(back_populates="field") #type: ignore