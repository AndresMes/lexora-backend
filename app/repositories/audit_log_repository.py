from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity
from app.models.audit_log import AuditLog

class AuditLogRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, log: AuditLog) -> AuditLog:
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        return log

    def get_by_id(self, log_id: UUID) -> Optional[AuditLog]:
        return self.session.get(AuditLog, log_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        stmt = (
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_by_filters(
        self,
        user_id: Optional[UUID] = None,
        action: Optional[AuditAction] = None,
        entity: Optional[AuditEntity] = None
    ) -> List[AuditLog]:

        stmt = select(AuditLog)

        if user_id:
            stmt = stmt.where(AuditLog.user_id == user_id)

        if action:
            stmt = stmt.where(AuditLog.action == action)

        if entity:
            stmt = stmt.where(AuditLog.entity == entity)

        stmt = stmt.order_by(AuditLog.created_at.desc())

        return self.session.exec(stmt).all()