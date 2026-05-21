from datetime import date

from fastapi import APIRouter, Depends, Query, UploadFile, File
from typing import List
from uuid import UUID

from app.schemas.requests.invoice_create import InvoiceSaveRequest
from app.services.interfaces.invoice_service_interface import InvoiceServiceInterface
from app.api.deps.invoice_service_dep import get_invoice_service

from app.schemas.responses.invoice_full import InvoiceFullRead



invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@invoice_router.post("/process")
async def process_invoice(
    file: UploadFile = File(...),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return await service.process_invoice(file)


@invoice_router.post("/save", response_model=InvoiceFullRead)
def save_invoice(
    data: InvoiceSaveRequest,  
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.save_invoice(data)


@invoice_router.get("/", response_model=List[InvoiceFullRead])
def list_invoices(
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.list_invoices()

@invoice_router.get("/by-date", response_model=List[InvoiceFullRead])
def get_invoices_by_date(
    start_date: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoices_by_date(start_date, end_date, skip, limit)


@invoice_router.get("/{invoice_id}", response_model=InvoiceFullRead)
def get_invoice_by_id(
    invoice_id: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoice_by_id(invoice_id)

@invoice_router.get("/provider/{provider_id}", response_model=List[InvoiceFullRead])
def get_invoices_by_provider(
    provider_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoices_by_provider(provider_id, skip, limit)


@invoice_router.get("/category/{category}", response_model=List[InvoiceFullRead])
def get_invoices_by_category(
    category: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoices_by_category(category, skip, limit)


@invoice_router.get("/status/{status}", response_model=List[InvoiceFullRead])
def get_invoices_by_status(
    status: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service)
):
    return service.get_invoices_by_status(status, skip, limit)