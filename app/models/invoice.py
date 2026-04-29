from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    provider_id: UUID = Field(foreign_key="parties.id", nullable=False)

    invoice_number: str = Field(nullable=False, max_length=100)
    issue_date: Optional[date] = None

    subtotal: Optional[float] = None
    iva: Optional[float] = None
    total: Optional[float] = None

    category: Optional[str] = Field(default=None, max_length=50)
    status: str = Field(default="PENDING", max_length=20)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    document: Optional["Document"] = Relationship(back_populates="invoice") # type: ignore
    provider: Optional["Party"] = Relationship(back_populates="invoices") #type: ignore

    items: list["InvoiceItem"] = Relationship(back_populates="invoice") # type: ignore
    extracted_fields: list["ExtractedField"] = Relationship(back_populates="invoice") # type: ignore