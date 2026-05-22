from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from app.enums.party_type_enum import PartyType

class PartyRead(BaseModel):
    id: UUID
    name: str
    nit: Optional[str]
    party_type: PartyType
    
    model_config = ConfigDict(from_attributes=True)
