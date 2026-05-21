from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class ExtractedFieldRead(BaseModel):
    id: UUID
    invoice_id: UUID

    field_name: str
    extracted_value: Optional[str]
    confidence: Optional[float]

    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)