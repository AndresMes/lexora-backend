import csv
import io
from typing import List
from datetime import date
from uuid import UUID

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from fastapi import HTTPException, UploadFile
from psycopg import IntegrityError

from xml.etree import ElementTree as ET

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
from app.utils.cloudinary_utils import upload_file


class InvoiceService(InvoiceServiceInterface):
    
    def __init__(self, invoice_repo: InvoiceRepository, party_service: PartyService, audit_repo: AuditLogRepository, user_repo: UserRepository, orchestator: InvoiceOrchestator):
        
        self.invoice_repo = invoice_repo
        self.party_service = party_service
        self.orchestator = orchestator
        self.audit_repo = audit_repo
        self.user_repo = user_repo
    
    async def process_invoice(self, file: UploadFile):
        file_bytes = await file.read()
        file_url = upload_file(file_bytes)
        result = await self.orchestator.process_invoice(file_bytes)
                
        return {
            "file_url": file_url,
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
        
    def export_invoice_csv(self, invoice: InvoiceFullRead) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["INFORMACIÓN DE LA FACTURA"])
        writer.writerow(["Número", "Fecha", "Categoría", "Subtotal", "IVA", "Total", "Estado"])
        writer.writerow([
            invoice.invoice.invoice_number,
            invoice.invoice.issue_date,
            invoice.invoice.category,
            invoice.invoice.subtotal,
            invoice.invoice.iva,
            invoice.invoice.total,
            invoice.invoice.status
        ])
        
        writer.writerow([])
        
        writer.writerow(["PROVEEDOR"])
        writer.writerow(["Nombre", "NIT", "Tipo"])
        writer.writerow([
            invoice.provider.name,
            invoice.provider.nit,
            invoice.provider.party_type
        ])
        
        writer.writerow([])
        
        writer.writerow(["ITEMS"])
        writer.writerow(["Descripción", "Cantidad", "Precio Unitario", "Total"])
        for item in invoice.items:
            writer.writerow([
                item.description,
                item.quantity,
                item.unit_price,
                item.total
            ])
        
        return output.getvalue()
    
    def export_invoice_xml(self, invoice: InvoiceFullRead) -> str:
        root = ET.Element("Invoice", xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2")
        root.set("xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        root.set("xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")

        # Encabezado
        ET.SubElement(root, "cbc:ID").text = invoice.invoice.invoice_number
        ET.SubElement(root, "cbc:IssueDate").text = str(invoice.invoice.issue_date)
        ET.SubElement(root, "cbc:InvoiceTypeCode").text = "01"
        ET.SubElement(root, "cbc:DocumentCurrencyCode").text = "COP"

        # Proveedor
        supplier = ET.SubElement(root, "cac:AccountingSupplierParty")
        party = ET.SubElement(supplier, "cac:Party")
        ET.SubElement(party, "cbc:Name").text = invoice.provider.name
        if invoice.provider.nit:
            tax_scheme = ET.SubElement(party, "cac:PartyTaxScheme")
            ET.SubElement(tax_scheme, "cbc:CompanyID").text = invoice.provider.nit

        # Totales
        monetary = ET.SubElement(root, "cac:LegalMonetaryTotal")
        ET.SubElement(monetary, "cbc:LineExtensionAmount", currencyID="COP").text = str(invoice.invoice.subtotal or 0)
        ET.SubElement(monetary, "cbc:TaxInclusiveAmount", currencyID="COP").text = str(invoice.invoice.total or 0)
        ET.SubElement(monetary, "cbc:PayableAmount", currencyID="COP").text = str(invoice.invoice.total or 0)

        # Items
        for i, item in enumerate(invoice.items, start=1):
            line = ET.SubElement(root, "cac:InvoiceLine")
            ET.SubElement(line, "cbc:ID").text = str(i)
            ET.SubElement(line, "cbc:InvoicedQuantity").text = str(item.quantity or 0)
            ET.SubElement(line, "cbc:LineExtensionAmount", currencyID="COP").text = str(item.total or 0)
            item_el = ET.SubElement(line, "cac:Item")
            ET.SubElement(item_el, "cbc:Description").text = item.description or ""
            price = ET.SubElement(line, "cac:Price")
            ET.SubElement(price, "cbc:PriceAmount", currencyID="COP").text = str(item.unit_price or 0)

        return ET.tostring(root, encoding="unicode", xml_declaration=False)
    
    def export_invoice_pdf(self, invoice: InvoiceFullRead) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )

        styles = getSampleStyleSheet()
        elements = []

        # ── Título ──
        title_style = ParagraphStyle(
            "title",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#1a1a2e"),
            spaceAfter=6
        )
        elements.append(Paragraph("FACTURA", title_style))
        elements.append(Paragraph(f"N° {invoice.invoice.invoice_number}", styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # ── Info general ──
        info_data = [
            ["Fecha de emisión", str(invoice.invoice.issue_date or "N/A")],
            ["Categoría", invoice.invoice.category or "N/A"],
            ["Estado", invoice.invoice.status],
            ["Proveedor", invoice.provider.name],
            ["NIT", invoice.provider.nit or "N/A"],
        ]
        info_table = Table(info_data, colWidths=[150, 300])
        info_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#444444")),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # ── Items ──
        elements.append(Paragraph("Detalle de Items", styles["Heading3"]))
        elements.append(Spacer(1, 8))

        item_headers = ["Descripción", "Cantidad", "Precio Unit.", "Total"]
        item_data = [item_headers] + [
            [
                item.description or "",
                str(item.quantity or 0),
                f"${item.unit_price:,.0f}" if item.unit_price else "N/A",
                f"${item.total:,.0f}" if item.total else "N/A"
            ]
            for item in invoice.items
        ]
        item_table = Table(item_data, colWidths=[220, 80, 100, 100])
        item_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))
        elements.append(item_table)
        elements.append(Spacer(1, 20))

        # ── Totales ──
        totals_data = [
            ["Subtotal", f"${invoice.invoice.subtotal:,.0f}" if invoice.invoice.subtotal else "N/A"],
            ["IVA", f"${invoice.invoice.iva:,.0f}" if invoice.invoice.iva else "N/A"],
            ["Total", f"${invoice.invoice.total:,.0f}" if invoice.invoice.total else "N/A"],
        ]
        totals_table = Table(totals_data, colWidths=[380, 120])
        totals_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("LINEABOVE", (0, -1), (-1, -1), 1, colors.HexColor("#1a1a2e")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(totals_table)

        doc.build(elements)
        return buffer.getvalue()