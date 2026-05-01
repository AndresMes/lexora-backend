from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class DocumentRead(BaseModel):
    id: UUID
    invoice_id: UUID

    file_url: str
    file_type: Optional[str]

    uploaded_at: datetime