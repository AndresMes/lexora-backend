from abc import ABC, abstractmethod

from app.schemas.responses.invoice_full import InvoiceFullRead


class InvoiceServiceInterface(ABC):

    @abstractmethod
    def process_invoice(self, file) -> InvoiceFullRead:
        pass

    @abstractmethod
    def save_invoice(self, data) -> InvoiceFullRead:
        pass