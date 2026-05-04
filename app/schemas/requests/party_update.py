from pydantic import BaseModel
from typing import Optional

class PartyUpdate(BaseModel):
    name: Optional[str] = None
    nit: Optional[str] = None
    party_type: Optional[str] = None