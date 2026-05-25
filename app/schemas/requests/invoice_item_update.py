from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class InvoiceItemUpdate(BaseModel):
    id: Optional[UUID] = None  
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None