from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity


class AuditLogFilter(BaseModel):
    user_id: Optional[UUID] = None
    action: Optional[AuditAction] = None
    entity: Optional[AuditEntity] = None