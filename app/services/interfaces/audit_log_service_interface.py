from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.schemas.filters.audit_log_filter import AuditLogFilter
from app.schemas.requests.audit_log_create import AuditLogCreate
from app.schemas.responses.audit_log_read import AuditLogRead

class AuditLogServiceInterface(ABC):
    
    @abstractmethod
    def create_log(self, dto: AuditLogCreate) -> AuditLogRead:
        pass
    
    @abstractmethod
    def get_by_id(self, log_id: UUID) -> AuditLogRead:
        pass
    
    @abstractmethod
    def get_all(self, skip, limit) -> List[AuditLogRead]:
        pass
    
    @abstractmethod
    def get_by_filters(self, filters: AuditLogFilter) -> List[AuditLogRead]:
        pass
    