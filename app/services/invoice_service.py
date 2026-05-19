###############################################################################################################################################

#                HAY QUE CAMBIAR Y VERIFICAR TODOS LOS METODOS DEL SERVICIO. ESTO ES SOLO UNA PRUEBA Y NO ES LA VERSIÓN FINAL

###############################################################################################################################################

from typing import List
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile
from psycopg import IntegrityError

from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity
from app.models.audit_log import AuditLog
from app.models.extracted_field import ExtractedField
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.orchestator.orchestator import InvoiceOrchestator
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.party_repository import PartyRepository
from app.schemas.requests.invoice_create import InvoiceSaveRequest
from app.schemas.responses.document_read import DocumentRead
from app.schemas.responses.extracted_field_read import ExtractedFieldRead
from app.schemas.responses.invoice_full import InvoiceFullRead

#Para eliminar luego si se dejan de usar
from app.schemas.responses.invoice_item_read import InvoiceItemRead
from app.schemas.responses.invoice_read import InvoiceRead
from app.schemas.responses.party_read import PartyRead
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.services.party_service import PartyService


class InvoiceService(InvoiceServiceInterface):
    
    def __init__(self, invoice_repo: InvoiceRepository, party_service: PartyService, audit_repo: AuditLogRepository, orchestator: InvoiceOrchestator):
        
        self.invoice_repo = invoice_repo
        self.party_service = party_service
        self.orchestator = orchestator
        self.audit_repo = audit_repo
    
    async def process_invoice(self, file: UploadFile):
        file_bytes = await file.read()
        result = await self.orchestator.process_invoice(file_bytes, file.filename)
        
        return {
            "filename": file.filename,
            "ocr_result": result
        }
    
    def save_invoice(self, data: InvoiceSaveRequest) -> InvoiceFullRead:
        # 1. Resolver el proveedor
        provider = self.party_service.get_or_create(
            name=data.provider.name,
            nit=data.provider.nit,
            party_type_arg=data.provider.party_type
        )

        # 2. Construir la Invoice con sus relaciones
        invoice = Invoice(
            user_id=data.user_id,
            provider_id=provider.id,
            invoice_number=data.invoice_number,
            issue_date=data.issue_date,
            subtotal=data.subtotal,
            iva=data.iva,
            total=data.total,
            category=data.category,
            status=data.status,
            items=[
                InvoiceItem(**item.model_dump())
                for item in data.items
            ],
            extracted_fields=[
                ExtractedField(**field.model_dump())
                for field in data.extracted_fields
            ]
        )

        # 3. Persistir (SQLModel cascadea items y extracted_fields)
        try:
            saved_invoice = self.invoice_repo.create(invoice)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe una factura con el número '{data.invoice_number}' para este proveedor."
            )

        # 4. Registrar AuditLog
        audit = AuditLog(
            user_id=data.user_id,
            action=AuditAction.CREATE,
            entity=AuditEntity.INVOICE,
            entity_id=saved_invoice.id
        )
        self.audit_repo.create(audit)

        # 5. Construir y retornar InvoiceFullRead
        return InvoiceFullRead(
            invoice=InvoiceRead.model_validate(saved_invoice),
            provider=PartyRead.model_validate(provider),
            items=[InvoiceItemRead.model_validate(i) for i in saved_invoice.items],
            document=DocumentRead.model_validate(saved_invoice.document) if saved_invoice.document else None,
            extracted_fields=[ExtractedFieldRead.model_validate(f) for f in saved_invoice.extracted_fields]
        )
    
    def list_invoices(self) -> List[InvoiceFullRead]:
        invoices = self.invoice_repo.get_all()
        
        return [
            InvoiceFullRead(
                invoice=InvoiceRead.model_validate(inv),
                provider=PartyRead.model_validate(inv.provider),
                items=[InvoiceItemRead.model_validate(i) for i in inv.items],
                document=DocumentRead.model_validate(inv.document) if inv.document else None,
                extracted_fields=[ExtractedFieldRead.model_validate(f) for f in inv.extracted_fields]
            )
            for inv in invoices
        ]
    
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