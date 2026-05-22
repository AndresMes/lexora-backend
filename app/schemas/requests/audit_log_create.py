from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AuditLogCreate(BaseModel):
    user_id: Optional[UUID] = None
    action: str
    entity: str
    entity_id: Optional[UUID] = None