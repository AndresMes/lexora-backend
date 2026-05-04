from fastapi import Depends

from app.api.deps.repo_deps import get_party_repo
from app.repositories.party_repository import PartyRepository
from app.services.party_service import PartyService


def get_party_service(
    party_repo: PartyRepository = Depends(get_party_repo),
) -> PartyRepository:

    return PartyService(
        party_repo=party_repo
    )