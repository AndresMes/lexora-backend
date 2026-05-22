from pydantic import BaseModel
from typing import Optional

class InvoiceUpdate(BaseModel):
    category: Optional[str] = None
    status: Optional[str] = None