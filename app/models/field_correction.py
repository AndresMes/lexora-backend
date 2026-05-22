from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class FieldCorrection(SQLModel, table=True):
    __tablename__ = "field_corrections"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    extracted_field_id: UUID = Field(foreign_key="extracted_fields.id", nullable=False)
    corrected_by: Optional[UUID] = Field(foreign_key="users.id")

    corrected_value: Optional[str] = None
    corrected_at: datetime = Field(default_factory=datetime.utcnow)

    field: Optional["ExtractedField"] = Relationship(back_populates="corrections") #type: ignore