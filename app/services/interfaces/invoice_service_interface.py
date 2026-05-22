from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.schemas.responses.invoice_full import InvoiceFullRead


class InvoiceServiceInterface(ABC):

    @abstractmethod
    async def process_invoice(self, file) -> InvoiceFullRead:
        pass

    @abstractmethod
    def save_invoice(self, data) -> InvoiceFullRead:
        pass
    
    @abstractmethod
    def list_invoices(self) -> List[InvoiceFullRead]:
        pass
    
    @abstractmethod
    def get_invoice_by_id(self, id: UUID) -> InvoiceFullRead:
        pass
    
    @abstractmethod
    def export_invoice_pdf(self, invoice: InvoiceFullRead) -> bytes:
        pass

    @abstractmethod
    def export_invoice_xml(self, invoice: InvoiceFullRead) -> str:
        pass

    @abstractmethod
    def export_invoice_csv(self, invoice: InvoiceFullRead) -> str:
        pass