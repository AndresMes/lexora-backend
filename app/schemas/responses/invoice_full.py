from pydantic import BaseModel
from typing import List, Optional
from .document_read import DocumentRead
from .extracted_field_read import ExtractedFieldRead
from .invoice_read import InvoiceRead
from .party_read import PartyRead
from .invoice_item_read import InvoiceItemRead


class InvoiceFullRead(BaseModel):
    invoice: InvoiceRead
    provider: PartyRead

    items: List[InvoiceItemRead]
    document: Optional[DocumentRead]

    extracted_fields: List[ExtractedFieldRead]

    class Config:
        orm_mode = True