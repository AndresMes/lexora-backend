from pydantic import BaseModel
from typing import Optional

from app.enums.party_type_enum import PartyType

class PartyCreate(BaseModel):
    name: str
    nit: Optional[str]
    party_type: PartyType
