from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Optional


class InvoiceItem(SQLModel, table=True):
    __tablename__ = "invoice_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    invoice_id: UUID = Field(foreign_key="invoices.id", nullable=False)

    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

    invoice: Optional["Invoice"] = Relationship(back_populates="items") #type: ignore