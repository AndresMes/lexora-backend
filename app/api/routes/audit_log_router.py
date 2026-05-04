from fastapi import APIRouter, Depends, Query
from typing import List
from uuid import UUID

from app.api.deps.audit_log_service_dep import get_audit_log_service
from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity
from app.schemas.filters.audit_log_filter import AuditLogFilter
from app.schemas.requests.audit_log_create import AuditLogCreate
from app.schemas.responses.audit_log_read import AuditLogRead
from app.services.interfaces.audit_log_service import AuditLogService

audit_router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@audit_router.post("/", response_model=AuditLogRead)
def create_log(
    dto: AuditLogCreate,
    service: AuditLogService = Depends(get_audit_log_service)
):
    return service.create_log(dto)


@audit_router.get("/", response_model=List[AuditLogRead])
def get_all_logs(
    skip: int = 0,
    limit: int = 100,
    service: AuditLogService = Depends(get_audit_log_service)
):
    return service.get_all(skip, limit)


@audit_router.get("/filters", response_model=List[AuditLogRead])
def get_logs_by_filters(
    user_id: UUID = Query(None),
    action: AuditAction = Query(None),
    entity: AuditEntity = Query(None),
    service: AuditLogService = Depends(get_audit_log_service)
):
    filters = AuditLogFilter(
        user_id=user_id,
        action=action,
        entity=entity
    )
    return service.get_by_filters(filters)


@audit_router.get("/{log_id}", response_model=AuditLogRead)
def get_log_by_id(
    log_id: UUID,
    service: AuditLogService = Depends(get_audit_log_service)
):
    return service.get_by_id(log_id)