from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from app.enums.party_type_enum import PartyType

class PartyRead(BaseModel):
    id: UUID
    name: str
    nit: Optional[str]
    party_type: PartyType
