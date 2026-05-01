from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ExtractedFieldCreate(BaseModel):
    invoice_id: UUID
    field_name: str
    extracted_value: Optional[str] = None
    confidence: Optional[float] = None