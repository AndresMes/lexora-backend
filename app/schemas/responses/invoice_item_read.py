from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class InvoiceItemRead(BaseModel):
    id: UUID
    invoice_id: UUID

    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total: Optional[float]