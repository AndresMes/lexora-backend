from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserRead(BaseModel):
    
    name: str
    id: UUID
    email: str
    created_at: datetime