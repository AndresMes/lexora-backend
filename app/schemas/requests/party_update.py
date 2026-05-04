from pydantic import BaseModel
from typing import Optional

from app.enums.party_type_enum import PartyType

class PartyUpdate(BaseModel):
    name: Optional[str] = None
    nit: Optional[str] = None
    party_type: Optional[PartyType] = None