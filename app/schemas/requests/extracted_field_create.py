from pydantic import BaseModel
from typing import Optional

class ExtractedFieldCreate(BaseModel):
    field_name: str
    extracted_value: Optional[str] = None
    confidence: Optional[float] = None