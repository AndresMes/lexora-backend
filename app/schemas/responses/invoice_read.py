from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime, date


class InvoiceRead(BaseModel):
    id: UUID
    user_id: UUID
    provider_id: UUID

    invoice_number: str
    issue_date: Optional[date]

    subtotal: Optional[float]
    iva: Optional[float]
    total: Optional[float]

    category: Optional[str]
    status: str

    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)