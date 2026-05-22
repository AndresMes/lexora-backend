from fastapi import HTTPException
from typing import List
from uuid import UUID

from app.models.audit_log import AuditLog
from app.repositories.audit_log_repository import AuditLogRepository
from app.schemas.filters.audit_log_filter import AuditLogFilter
from app.schemas.requests.audit_log_create import AuditLogCreate
from app.schemas.responses.audit_log_read import AuditLogRead

class AuditLogService:

    def __init__(self, audit_log_repo: AuditLogRepository):
        self.audit_log_repo = audit_log_repo

    def create_log(self, dto: AuditLogCreate) -> AuditLogRead:

        log = AuditLog(
            user_id=dto.user_id,
            action=dto.action,
            entity=dto.entity,
            entity_id=dto.entity_id
        )

        saved = self.audit_log_repo.create(log)

        return self._to_read(saved)

    def get_by_id(self, log_id: UUID) -> AuditLogRead:

        log = self.audit_log_repo.get_by_id(log_id)

        if not log:
            raise HTTPException(status_code=404, detail="Log de auditorio no encontrado")

        return self._to_read(log)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLogRead]:
        logs = self.audit_log_repo.get_all(skip, limit)
        return [self._to_read(l) for l in logs]

    def get_by_filters(self, filters: AuditLogFilter) -> List[AuditLogRead]:

        logs = self.audit_log_repo.get_by_filters(
            user_id=filters.user_id,
            action=filters.action,
            entity=filters.entity
        )

        return [self._to_read(l) for l in logs]

    def _to_read(self, log: AuditLog) -> AuditLogRead:
        return AuditLogRead(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            entity=log.entity,
            entity_id=log.entity_id,
            created_at=log.created_at
        )