from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.models import ExtractedField


class ExtractedFieldRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_invoice(self, invoice_id: UUID) -> List[ExtractedField]:
        stmt = select(ExtractedField).where(
            ExtractedField.invoice_id == invoice_id
        )
        return self.session.exec(stmt).all()

    def create(self, field: ExtractedField) -> ExtractedField:
        self.session.add(field)
        self.session.commit()
        self.session.refresh(field)
        return field

    def create_many(self, fields: List[ExtractedField]) -> List[ExtractedField]:
        self.session.add_all(fields)
        self.session.commit()
        for field in fields:
            self.session.refresh(field)
        return fields

    def delete_by_invoice(self, invoice_id: UUID) -> None:
        fields = self.get_by_invoice(invoice_id)
        for field in fields:
            self.session.delete(field)
        self.session.commit()