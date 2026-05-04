from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from app.api.deps.party_service_dep import get_party_service
from app.schemas.requests.party_create import PartyCreate
from app.schemas.requests.party_update import PartyUpdate
from app.schemas.responses.party_read import PartyRead
from app.services.interfaces.party_service_interface import PartyServiceInterface

party_router = APIRouter(prefix="/parties", tags=["Parties"])


@party_router.post("/", response_model=PartyRead)
def create_party(
    party_dto: PartyCreate,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.create_party(party_dto)


@party_router.get("/", response_model=List[PartyRead])
def get_party_all(
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.get_all()


# 🔥 RUTAS ESPECÍFICAS PRIMERO
@party_router.get("/nit/{nit}", response_model=PartyRead)
def get_party_by_nit(
    nit: str,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.get_by_nit(nit)


@party_router.get("/type/{party_type}", response_model=List[PartyRead])
def get_parties_by_type(
    party_type: str,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.get_by_type(party_type)


@party_router.get("/search-name/{party_name}", response_model=List[PartyRead])
def get_parties_by_name(
    party_name: str,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.search_by_name(party_name)


# 🔥 AL FINAL (genérica)
@party_router.get("/{id_party}", response_model=PartyRead)
def get_party_by_id(
    id_party: UUID,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.get_by_id(id_party)


@party_router.put("/{id_party}", response_model=PartyRead)
def update_party(
    id_party: UUID,
    dto: PartyUpdate,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.update_party(id_party, dto)


@party_router.delete("/{id_party}")
def delete_party(
    id_party: UUID,
    service: PartyServiceInterface = Depends(get_party_service)
):
    return service.delete_party(id_party)