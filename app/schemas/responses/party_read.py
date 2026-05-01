from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PartyRead(BaseModel):
    id: UUID
    name: str
    nit: Optional[str]
    party_type: Optional[str]
