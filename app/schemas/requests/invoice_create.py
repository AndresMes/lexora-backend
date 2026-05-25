from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import date

from app.schemas.requests.extracted_field_create import ExtractedFieldCreate
from app.schemas.requests.invoice_item_create import InvoiceItemCreate
from app.schemas.requests.party_create import PartyCreate


class InvoiceSaveRequest(BaseModel):
    user_id: UUID
    invoice_number: str
    issue_date: Optional[date] = None
    subtotal: Optional[float] = None
    iva: Optional[float] = None
    total: Optional[float] = None
    category: Optional[str] = None
    status: str = "PENDING"
    
    file_url: Optional[str] = None     
    file_type: Optional[str] = None

    provider: PartyCreate
    items: List[InvoiceItemCreate] = []
    extracted_fields: List[ExtractedFieldCreate] = []