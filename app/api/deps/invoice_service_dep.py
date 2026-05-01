from fastapi import Depends
from app.api.deps.repo_deps import get_invoice_repo, get_party_repo
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.party_repository import PartyRepository
from app.services.invoice_service import InvoiceService
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface

def get_invoice_service(
    invoice_repo: InvoiceRepository = Depends(get_invoice_repo),
    party_repo: PartyRepository = Depends(get_party_repo),
) -> InvoiceServiceInterface:

    return InvoiceService(
        invoice_repo=invoice_repo,
        party_repo=party_repo
    )