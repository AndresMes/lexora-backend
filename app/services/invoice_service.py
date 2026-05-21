from typing import List
from datetime import date
from uuid import UUID

from fastapi import HTTPException, UploadFile
from psycopg import IntegrityError

from app.enums.audit_action_enum import AuditAction
from app.enums.audit_entity import AuditEntity
from app.enums.party_type_enum import PartyType
from app.models.audit_log import AuditLog
from app.models.extracted_field import ExtractedField
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.orchestator.orchestator import InvoiceOrchestator
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.user_repository import UserRepository
from app.schemas.requests.invoice_create import InvoiceSaveRequest
from app.schemas.responses.document_read import DocumentRead
from app.schemas.responses.extracted_field_read import ExtractedFieldRead
from app.schemas.responses.invoice_full import InvoiceFullRead

from app.schemas.responses.invoice_item_read import InvoiceItemRead
from app.schemas.responses.invoice_read import InvoiceRead
from app.schemas.responses.party_read import PartyRead
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.services.party_service import PartyService


class InvoiceService(InvoiceServiceInterface):
    
    def __init__(self, invoice_repo: InvoiceRepository, party_service: PartyService, audit_repo: AuditLogRepository, user_repo: UserRepository, orchestator: InvoiceOrchestator):
        
        self.invoice_repo = invoice_repo
        self.party_service = party_service
        self.orchestator = orchestator
        self.audit_repo = audit_repo
        self.user_repo = user_repo
    
    async def process_invoice(self, file: UploadFile):
        file_bytes = await file.read()
        result = await self.orchestator.process_invoice(file_bytes, file.filename)
        
        return {
            "filename": file.filename,
            "ocr_result": result
        }
    
    def save_invoice(self, data: InvoiceSaveRequest) -> InvoiceFullRead:

        # 1. Verificar que el usuario existe
        user = self.user_repo.get_by_id(data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        # 2. Verificar que el party_type es válido
        valid_party_types = {PartyType.DISTRIBUTOR, PartyType.CLIENT}
        if data.provider.party_type not in valid_party_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de proveedor inválido. Debe ser uno de: {[p.value for p in valid_party_types]}"
            )

        # 3. Verificar que el invoice_number no esté vacío
        if not data.invoice_number.strip():
            raise HTTPException(status_code=400, detail="El número de factura no puede estar vacío.")

        # 4. Verificar que el total sea consistente con subtotal + iva
        if data.subtotal is not None and data.iva is not None and data.total is not None:
            expected_total = round(data.subtotal + data.iva, 2)
            if round(data.total, 2) != expected_total:
                raise HTTPException(
                    status_code=400,
                    detail=f"El total ({data.total}) no coincide con subtotal + iva ({expected_total})."
                )

        # 5. Verificar que los items tengan montos positivos
        for i, item in enumerate(data.items):
            if item.quantity is not None and item.quantity <= 0:
                raise HTTPException(status_code=400, detail=f"El item {i+1} tiene una cantidad inválida.")
            if item.unit_price is not None and item.unit_price < 0:
                raise HTTPException(status_code=400, detail=f"El item {i+1} tiene un precio unitario negativo.")

        # 6. Resolver el proveedor
        provider = self.party_service.get_or_create(
            name=data.provider.name,
            nit=data.provider.nit,
            party_type_arg=data.provider.party_type
        )

        # 7. Construir la Invoice con sus relaciones
        invoice = Invoice(
            user_id=data.user_id,
            provider_id=provider.id,
            invoice_number=data.invoice_number.strip(),
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

        # 8. Persistir
        try:
            saved_invoice = self.invoice_repo.create(invoice)
        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe una factura con el número '{data.invoice_number}' para este proveedor."
            )

        # 9. Registrar AuditLog
        audit = AuditLog(
            user_id=data.user_id,
            action=AuditAction.CREATE,
            entity=AuditEntity.INVOICE,
            entity_id=saved_invoice.id
        )
        self.audit_repo.create(audit)

        # 10. Construir y retornar InvoiceFullRead
        return InvoiceFullRead(
            invoice=InvoiceRead.model_validate(saved_invoice),
            provider=PartyRead.model_validate(provider),
            items=[InvoiceItemRead.model_validate(i) for i in saved_invoice.items],
            document=DocumentRead.model_validate(saved_invoice.document) if saved_invoice.document else None,
            extracted_fields=[ExtractedFieldRead.model_validate(f) for f in saved_invoice.extracted_fields]
        )
    
    def list_invoices(self) -> List[InvoiceFullRead]:
        invoices = self.invoice_repo.get_all()
        
        return [self._to_full_read(inv) for inv in invoices]
    
    def get_invoice_by_id(self, id: UUID) -> InvoiceFullRead:
        invoice = self.invoice_repo.get_by_id(id)

        if not invoice:
            raise HTTPException(status_code=404, detail="Factura no encontrada")

        return self._to_full_read(invoice)

    def get_invoices_by_date(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
    
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor a la fecha de fin.")

        invoices = self.invoice_repo.get_by_issue_date_range(start_date, end_date, skip, limit)

        return [self._to_full_read(inv) for inv in invoices]
        
    def get_invoices_by_provider(self, provider_id: UUID, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        provider = self.party_service.get_by_id(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado.")

        invoices = self.invoice_repo.get_by_provider_id(provider_id, skip, limit)
        return [self._to_full_read(inv) for inv in invoices]

    def get_invoices_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        if not category.strip():
            raise HTTPException(status_code=400, detail="La categoría no puede estar vacía.")

        invoices = self.invoice_repo.get_by_category(category.strip(), skip, limit)
        return [self._to_full_read(inv) for inv in invoices]

    def get_invoices_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[InvoiceFullRead]:
        valid_statuses = {"PENDING", "APPROVED", "REJECTED"}
        if status.upper() not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Estado inválido. Debe ser uno de: {valid_statuses}"
            )

        invoices = self.invoice_repo.get_by_status(status.upper(), skip, limit)
        return [self._to_full_read(inv) for inv in invoices]
    
    def _to_full_read(self, invoice: Invoice) -> InvoiceFullRead:
        return InvoiceFullRead(
            invoice=InvoiceRead.model_validate(invoice),
            provider=PartyRead.model_validate(invoice.provider),
            items=[InvoiceItemRead.model_validate(i) for i in invoice.items],
            document=DocumentRead.model_validate(invoice.document) if invoice.document else None,
            extracted_fields=[ExtractedFieldRead.model_validate(f) for f in invoice.extracted_fields]
        )