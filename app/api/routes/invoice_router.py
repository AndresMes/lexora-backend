from fastapi import APIRouter, Depends, UploadFile, File
from typing import List
from uuid import UUID

from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.api.deps.invoice_service_dep import get_invoice_service

from app.schemas.responses.invoice_full import InvoiceFullRead



invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@invoice_router.post("/process", response_model=InvoiceFullRead)
def process_invoice(
    file: UploadFile = File(...),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.process_invoice(file)


@invoice_router.post("/save", response_model=InvoiceFullRead)
def save_invoice(
    data: dict,  
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.save_invoice(data)


@invoice_router.get("/", response_model=List[InvoiceFullRead])
def list_invoices(
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.list_invoices()


@invoice_router.get("/{invoice_id}", response_model=InvoiceFullRead)
def get_invoice_by_id(
    invoice_id: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoice_by_id(invoice_id)