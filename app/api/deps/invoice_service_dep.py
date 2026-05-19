from fastapi import Depends
from app.api.deps.orchestator_dep import get_orchestator
from app.api.deps.party_service_dep import get_party_service
from app.api.deps.repo_deps import get_audit_log_repo, get_invoice_repo
from app.orchestator.orchestator import InvoiceOrchestator
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.services.invoice_service import InvoiceService
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.services.party_service import PartyService

def get_invoice_service(
    invoice_repo: InvoiceRepository = Depends(get_invoice_repo),
    party_service: PartyService = Depends(get_party_service),
    audit_repo: AuditLogRepository = Depends(get_audit_log_repo),
    orchestator: InvoiceOrchestator = Depends(get_orchestator)
) -> InvoiceServiceInterface:

    return InvoiceService(
        invoice_repo=invoice_repo,
        party_service=party_service,
        audit_repo=audit_repo,
        orchestator = orchestator
    )