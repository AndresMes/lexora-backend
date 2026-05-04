from fastapi import HTTPException
from uuid import UUID
from typing import List

from app.models.party import Party
from app.repositories.party_repository import PartyRepository
from app.schemas.requests.party_create import PartyCreate
from app.schemas.responses.party_read import PartyRead
from app.services.interfaces.party_service_interface import PartyServiceInterface

class PartyService(PartyServiceInterface):

    def __init__(self, party_repo: PartyRepository):
        self.party_repo = party_repo

    def get_by_id(self, id_party: UUID) -> PartyRead:
        party = self.party_repo.get_by_id(id_party)

        if not party:
            raise HTTPException(status_code=404, detail="Party not found")

        return self._to_read(party)

    def get_by_nit(self, nit: str) -> PartyRead:
        party = self.party_repo.get_by_nit(nit)

        if not party:
            raise HTTPException(status_code=404, detail="Party not found")

        return self._to_read(party)

    def get_all(self) -> List[PartyRead]:
        parties = self.party_repo.get_all()
        return [self._to_read(p) for p in parties]

    def get_by_type(self, party_type: str) -> List[PartyRead]:
        parties = self.party_repo.get_by_type(party_type)
        return [self._to_read(p) for p in parties]

    def search_by_name(self, name: str) -> List[PartyRead]:
        parties = self.party_repo.search_by_name(name)
        return [self._to_read(p) for p in parties]

    def create_party(self, party_dto: PartyCreate) -> PartyRead:

        if not party_dto.name:
            raise HTTPException(status_code=400, detail="Name is required")

        if party_dto.nit:
            existing = self.party_repo.get_by_nit(party_dto.nit)
            if existing:
                return self._to_read(existing)

        party = Party(
            name=party_dto.name.strip(),
            nit=party_dto.nit,
            party_type=party_dto.party_type or "UNKNOWN"
        )

        saved = self.party_repo.create(party)

        return self._to_read(saved)
    
    def update_party(self, id_party, dto):
        party = self.party_repo.get_by_id(id_party)

        if not party:
            raise HTTPException(status_code=404, detail="Party not found")

        if dto.nit and dto.nit != party.nit:
            existing = self.party_repo.get_by_nit(dto.nit)
            if existing and existing.id != id_party:
                raise HTTPException(status_code=409, detail="NIT already exists")

        # Actualización parcial
        if dto.name is not None:
            party.name = dto.name.strip()

        if dto.nit is not None:
            party.nit = dto.nit

        if dto.party_type is not None:
            party.party_type = dto.party_type

        updated = self.party_repo.update(party)

        return self._to_read(updated)

    def delete_party(self, id_party: UUID):

        party = self.party_repo.get_by_id(id_party)

        if not party:
            raise HTTPException(status_code=404, detail="Party not found")

        self.party_repo.delete(party)

        return {"message": "Party deleted successfully"}

    def _to_read(self, party: Party) -> PartyRead:
        return PartyRead(
            id=party.id,
            name=party.name,
            nit=party.nit,
            party_type=party.party_type
        )