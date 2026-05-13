###############################################################################################################################################

#                HAY QUE CAMBIAR Y VERIFICAR TODOS LOS METODOS DEL SERVICIO. ESTO ES SOLO UNA PRUEBA Y NO ES LA VERSIÓN FINAL

###############################################################################################################################################

from typing import List
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile

from app.orchestator.orchestator import InvoiceOrchestator
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.party_repository import PartyRepository
from app.schemas.responses.document_read import DocumentRead
from app.schemas.responses.extracted_field_read import ExtractedFieldRead
from app.schemas.responses.invoice_full import InvoiceFullRead

#Para eliminar luego si se dejan de usar
from app.schemas.responses.invoice_item_read import InvoiceItemRead
from app.schemas.responses.invoice_read import InvoiceRead
from app.schemas.responses.party_read import PartyRead
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface


class InvoiceService(InvoiceServiceInterface):
    
    def __init__(self, invoice_repo: InvoiceRepository, party_repo: PartyRepository, orchestator: InvoiceOrchestator):
        
        self.invoice_repo = invoice_repo
        self.party_repo = party_repo
        self.orchestator = orchestator
    
    async def process_invoice(self, file: UploadFile) -> InvoiceFullRead:
        file_bytes = await file.read()
        result = await self.orchestator.process_invoice(file_bytes, file.filename)
        return self.fake_invoice()
    
    def save_invoice(self, data) -> InvoiceFullRead:
        return self.fake_invoice()
    
    def list_invoices(self) -> List[InvoiceFullRead]:
        return self.invoice_repo.get_all()
    
    def get_invoice_by_id(self, id: UUID) -> InvoiceFullRead:
        invoice = self.invoice_repo.get_by_id(id)

        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        return self._fake_invoice()  # 🔥 temporal
            
    #SOLO MIENTRAS SE IMPLEMENTA HACEMOS UN DATO CONSTANTE
    
    def fake_invoice(self) -> InvoiceFullRead:
        

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
                party_type="DISTRIBUTOR"
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