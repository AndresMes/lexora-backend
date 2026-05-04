from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity

class AuditLogRead(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: AuditAction
    entity: AuditEntity
    entity_id: Optional[UUID]
    created_at: datetime