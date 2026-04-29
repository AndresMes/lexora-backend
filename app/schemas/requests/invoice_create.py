from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date


class InvoiceCreate(BaseModel):
    provider_id: UUID
    invoice_number: str
    issue_date: Optional[date] = None

    subtotal: Optional[float] = None
    iva: Optional[float] = None
    total: Optional[float] = None

    category: Optional[str] = None