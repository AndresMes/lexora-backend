from abc import ABC, abstractmethod
from datetime import date
from typing import List
from uuid import UUID

from app.schemas.requests.invoice_update import InvoiceUpdate
from app.schemas.responses.invoice_full import InvoiceFullRead


class InvoiceServiceInterface(ABC):

    @abstractmethod
    async def process_invoice(self, file) -> InvoiceFullRead:
        pass

    @abstractmethod
    def save_invoice(self, data) -> InvoiceFullRead:
        pass
    
    @abstractmethod
    def list_invoices(self, user_id: UUID) -> List[InvoiceFullRead]:
        pass
    
    @abstractmethod
    def get_invoice_by_id(self, user_id: UUID, id: UUID) -> InvoiceFullRead:
        pass
    
    @abstractmethod
    def export_invoice_pdf(self, invoice: InvoiceFullRead) -> bytes:
        pass
    
    @abstractmethod
    def get_invoices_by_date(self, user_id:UUID, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        pass
    
    @abstractmethod
    def get_invoices_by_provider(self, user_id:UUID, provider_id: UUID, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        pass
    
    @abstractmethod
    def get_invoices_by_category(self, user_id:UUID, category: str, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        pass
    
    @abstractmethod
    def get_invoices_by_status(self, user_id:UUID, status: str, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        pass


    @abstractmethod
    def export_invoice_xml(self, invoice: InvoiceFullRead) -> str:
        pass

    @abstractmethod
    def export_invoice_csv(self, invoice: InvoiceFullRead) -> str:
        pass
    
    @abstractmethod
    def update_invoice(self, id: UUID, dto: InvoiceUpdate) -> InvoiceFullRead:
        pass

    @abstractmethod
    def update_invoice_status(self, id: UUID, status: str) -> InvoiceFullRead:
        pass
    
    @abstractmethod
    def delete_invoice_by_id(self, user_id: UUID, invoice_id: UUID):
        pass