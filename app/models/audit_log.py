from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: Optional[UUID] = Field(foreign_key="users.id")

    action: Optional[str] = Field(max_length=50)
    entity: Optional[str] = Field(max_length=50)
    entity_id: Optional[UUID]

    created_at: datetime = Field(default_factory=datetime.utcnow)