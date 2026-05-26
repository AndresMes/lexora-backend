from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile, File
from typing import List
from uuid import UUID

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.requests.invoice_create import InvoiceSaveRequest
from app.schemas.requests.invoice_update import InvoiceUpdate
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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.list_invoices(current_user.id, skip, limit)

@invoice_router.get("/by-date", response_model=List[InvoiceFullRead])
def get_invoices_by_date(
    start_date: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_invoices_by_date(current_user.id, start_date, end_date, skip, limit)


@invoice_router.get("/{invoice_id}", response_model=InvoiceFullRead)
def get_invoice_by_id(
    invoice_id: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(current_user.id, invoice_id)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta factura")
    return invoice

@invoice_router.get("/provider/{provider_id}", response_model=List[InvoiceFullRead])
def get_invoices_by_provider(
    provider_id: UUID,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_invoices_by_provider(current_user.id, provider_id, skip, limit)


@invoice_router.get("/category/{category}", response_model=List[InvoiceFullRead])
def get_invoices_by_category(
    category: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_invoices_by_category(current_user.id, category, skip, limit)



@invoice_router.get("/status/{status}", response_model=List[InvoiceFullRead])
def get_invoices_by_status(
    status: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.get_invoices_by_status(current_user.id, status, skip, limit)

@invoice_router.patch("/{id_invoice}/status")
def update_invoice_status(
    id_invoice: UUID,
    status: str = Query(...),
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(current_user.id,id_invoice)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta factura")
    return service.update_invoice_status(current_user.id, id_invoice, status)

@invoice_router.patch("/{id_invoice}", response_model=InvoiceFullRead)
def update_invoice(
    id_invoice: UUID,
    dto: InvoiceUpdate,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(current_user.id,id_invoice)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta factura")
    return service.update_invoice(current_user.id, id_invoice, dto)
    

@invoice_router.get("/{id_invoice}/export/csv")
def export_csv(
    id_invoice: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(id_invoice)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para exportar esta factura")
    
    csv_content = service.export_invoice_csv(invoice)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=factura_{invoice.invoice.invoice_number}.csv"}
    )

@invoice_router.get("/{id_invoice}/export/xml")
def export_xml(
    id_invoice: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(id_invoice)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para exportar esta factura")
    
    xml_content = service.export_invoice_xml(invoice)
    return Response(
        content=xml_content,
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename=factura_{invoice.invoice.invoice_number}.xml"}
    )

@invoice_router.get("/{id_invoice}/export/pdf")
def export_pdf(
    id_invoice: UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    invoice = service.get_invoice_by_id(id_invoice)
    if invoice.invoice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para exportar esta factura")
    
    pdf_content = service.export_invoice_pdf(invoice)
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=factura_{invoice.invoice.invoice_number}.pdf"}
    )

@invoice_router.delete("/{id_invoice}")
def delete_invoice(
    id_invoice:UUID,
    service: InvoiceServiceInterface = Depends(get_invoice_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete_invoice_by_id(current_user.id, id_invoice)
    