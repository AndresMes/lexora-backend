from datetime import date
from uuid import UUID

from pydantic import BaseModel
from typing import List, Optional

from app.schemas.requests.invoice_item_update import InvoiceItemUpdate

class InvoiceUpdate(BaseModel):
    category: Optional[str] = None
    issue_date: Optional[date] = None
    subtotal: Optional[float] = None
    iva: Optional[float] = None
    total: Optional[float] = None
    items: Optional[List[InvoiceItemUpdate]] = None
    delete_items: Optional[List[UUID]] = None