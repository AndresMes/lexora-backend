from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime


class DocumentRead(BaseModel):
    id: UUID
    invoice_id: UUID

    file_url: str
    file_type: Optional[str]

    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)