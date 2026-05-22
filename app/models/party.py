from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional

from app.enums.party_type_enum import PartyType

class Party(SQLModel, table=True):

    __tablename__ = "parties"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(nullable=False, max_length=250)
    nit: Optional[str] = Field(max_length=250)
    party_type: PartyType = Field(max_length=20)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    invoices: list["Invoice"] = Relationship(back_populates="provider") #type: ignore