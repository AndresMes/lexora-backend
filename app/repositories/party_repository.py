from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select
from ..models.party import Party


class PartyRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, party: Party) -> Party:
        self.session.add(party)
        self.session.commit()
        self.session.refresh(party)
        return party

    def get_by_id(self, party_id: UUID) -> Optional[Party]:
        return self.session.get(Party, party_id)

    def get_by_nit(self, nit: str) -> Optional[Party]:
        stmt = select(Party).where(Party.nit == nit)
        return self.session.exec(stmt).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Party]:
        stmt = (
            select(Party)
            .order_by(Party.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def get_by_type(self, party_type_arg: str, skip: int = 0, limit: int = 100) -> List[Party]:
        stmt = (
            select(Party)
            .where(Party.party_type == party_type_arg)
            .order_by(Party.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def search_by_name(self, name: str) -> List[Party]:
        stmt = select(Party).where(Party.name.ilike(f"%{name}%"))
        return self.session.exec(stmt).all()

    def get_or_create(self, name: str, nit: Optional[str], party_type_arg: str) -> Party:
        if nit:
            existing = self.get_by_nit(nit)
            if existing:
                return existing

        party = Party(
            name=name,
            nit=nit,
            party_type=party_type_arg
        )

        return self.create(party)
    
    def update(self, party: Party) -> Party:
        self.session.add(party)
        self.session.commit()
        self.session.refresh(party)
        return party

    def delete(self, party: Party) -> None:
        self.session.delete(party)
        self.session.commit()