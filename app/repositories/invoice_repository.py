from sqlmodel import Session, select
from typing import Optional, List
from ..models.invoice import Invoice
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import selectinload

class InvoiceRepository:

    def __init__(self, session: Session):
        self.session = session

    def _base_query(self):
        return (
            select(Invoice)
            .options(
                selectinload(Invoice.provider),
                selectinload(Invoice.items),
                selectinload(Invoice.extracted_fields),
                selectinload(Invoice.document)
            )
        )

    def get_by_id(self, invoice_id: UUID) -> Optional[Invoice]:
        stmt = self._base_query().where(Invoice.id == invoice_id)
        return self.session.exec(stmt).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = self._base_query().order_by(Invoice.created_at.desc()).offset(skip).limit(limit)
        return self.session.exec(stmt).all()

    def get_by_created_at_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            self._base_query()
            .where(Invoice.created_at >= start_date)
            .where(Invoice.created_at <= end_date)
            .order_by(Invoice.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_by_provider_id(self, provider_id: UUID, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            self._base_query()
            .where(Invoice.provider_id == provider_id)
            .order_by(Invoice.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            self._base_query()
            .where(Invoice.category == category)
            .order_by(Invoice.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Invoice]:
        stmt = (
            self._base_query()
            .where(Invoice.status == status)
            .order_by(Invoice.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def create(self, invoice: Invoice) -> Invoice:
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        # Recargar con relaciones después del commit
        stmt = self._base_query().where(Invoice.id == invoice.id)
        return self.session.exec(stmt).first()

    def update(self, invoice: Invoice) -> Invoice:
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        stmt = self._base_query().where(Invoice.id == invoice.id)
        return self.session.exec(stmt).first()

    def delete(self, invoice: Invoice):
        self.session.delete(invoice)
        self.session.commit()