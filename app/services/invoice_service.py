import datetime
from uuid import uuid4

from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.party_repository import PartyRepository
from app.schemas.responses.invoice_full import InvoiceFullRead
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface


class InvoiceService(InvoiceServiceInterface):
    
    def __init__(self, invoice_repo: InvoiceRepository, party_repo: PartyRepository):
        
        self.invoice_repo = invoice_repo
        self.party_repo = party_repo
    
    def process_invoice(self, file) -> InvoiceFullRead:
        return self.__fake_invoice()
    
    def save_invoice(self, data) -> InvoiceFullRead:
        return self.__fake_invoice()
    
    #SOLO MIENTRAS SE IMPLEMENTA HACEMOS UN DATO CONSTANTE
    
    def _fake_invoice(self) -> InvoiceFullRead:
        from ..schemas.responses import (
            InvoiceRead, PartyRead, InvoiceItemRead,
            DocumentRead, ExtractedFieldRead
        )

        return InvoiceFullRead(
            invoice=InvoiceRead(
                id=uuid4(),
                user_id=uuid4(),
                provider_id=uuid4(),
                invoice_number="INV-001",
                issue_date=None,
                subtotal=1000,
                iva=190,
                total=1190,
                category="SERVICES",
                status="PENDING",
                created_at=datetime.utcnow()
            ),
            provider=PartyRead(
                id=uuid4(),
                name="ACME Corp",
                nit="123456",
                party_type="PROVIDER"
            ),
            items=[
                InvoiceItemRead(
                    id=uuid4(),
                    invoice_id=uuid4(),
                    description="Producto A",
                    quantity=2,
                    unit_price=500,
                    total=1000
                )
            ],
            document=DocumentRead(
                id=uuid4(),
                invoice_id=uuid4(),
                file_url="s3://file.pdf",
                file_type="pdf",
                uploaded_at=datetime.utcnow()
            ),
            extracted_fields=[
                ExtractedFieldRead(
                    id=uuid4(),
                    invoice_id=uuid4(),
                    field_name="total",
                    extracted_value="1190",
                    confidence=0.95,
                    created_at=datetime.utcnow()
                )
            ]
        )