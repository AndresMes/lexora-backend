from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class InvoiceItemRead(BaseModel):
    id: UUID
    invoice_id: UUID

    description: Optional[str]
    quantity: Optional[float]
    unit_price: Optional[float]
    total: Optional[float]
    
    model_config = ConfigDict(from_attributes=True)