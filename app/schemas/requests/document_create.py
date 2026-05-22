from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DocumentCreate(BaseModel):
    invoice_id: UUID
    file_url: str
    file_type: Optional[str] = None