from pydantic import BaseModel
from typing import Optional

class PartyCreate(BaseModel):
    name: str
    nit: Optional[str]
    party_type: Optional[str]
