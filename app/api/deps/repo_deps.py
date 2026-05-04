from fastapi import Depends
from sqlmodel import Session

from app.api.deps.db_session import get_db
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.party_repository import PartyRepository
from app.repositories.user_repository import UserRepository


def get_invoice_repo(session: Session = Depends(get_db)):
    return InvoiceRepository(session)


def get_party_repo(session: Session = Depends(get_db)):
    return PartyRepository(session)

def get_user_repo(session: Session = Depends(get_db)):
    return UserRepository(session)

def get_party_repo(session: Session = Depends(get_db)):
    return PartyRepository