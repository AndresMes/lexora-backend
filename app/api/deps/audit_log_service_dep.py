from fastapi import Depends

from app.api.deps.repo_deps import get_audit_log_repo
from app.repositories.audit_log_repository import AuditLogRepository
from app.services.audit_log_service_interface import AuditLogServiceInterface
from app.services.interfaces.audit_log_service import AuditLogService


def get_audit_log_service(
    audit_log_repo: AuditLogRepository = Depends(get_audit_log_repo),
) -> AuditLogServiceInterface:

    return AuditLogService(
        audit_log_repo=audit_log_repo
    )