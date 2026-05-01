from sqlmodel import Session, select
from ..models.document import Document
from uuid import UUID
from typing import Optional, List


class DocumentRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        stmt = select(Document).order_by(Document.uploaded_at.desc()).offset(skip).limit(limit)
        return self.session.exec(stmt).all()

    def get_by_invoice(self, invoice_id: UUID) -> Optional[Document]:
        stmt = select(Document).where(Document.invoice_id == invoice_id)
        return self.session.exec(stmt).first()

    def create(self, document: Document) -> Document:
        self.session.add(document)
        self.session.commit()
        self.session.refresh(document)
        return document
    