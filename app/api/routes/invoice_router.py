from fastapi import APIRouter, Depends, UploadFile, File
from typing import List
from uuid import UUID

from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.api.deps.invoice_service_dep import get_invoice_service

from app.schemas.responses.invoice_full import InvoiceFullRead

invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


# 🔹 1. Procesar factura (OCR + LLM - por ahora fake)
@invoice_router.post("/process", response_model=InvoiceFullRead)
def process_invoice(
    file: UploadFile = File(...),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.process_invoice(file)


# 🔹 2. Guardar factura (confirmación del usuario)
@invoice_router.post("/save", response_model=InvoiceFullRead)
def save_invoice(
    data: dict,  # luego lo cambias por InvoiceSave
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.save_invoice(data)


# 🔹 3. Listar facturas
@invoice_router.get("/", response_model=List[InvoiceFullRead])
def list_invoices(
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.list_invoices()


# 🔹 4. Obtener factura por ID
@invoice_router.get("/{invoice_id}", response_model=InvoiceFullRead)
def get_invoice_by_id(
    invoice_id: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoice_by_id(invoice_id)