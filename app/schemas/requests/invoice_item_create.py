from typing import Optional

from pydantic import BaseModel


class InvoiceItemCreate(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None