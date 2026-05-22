from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.schemas.requests.party_create import PartyCreate
from app.schemas.requests.party_update import PartyUpdate
from app.schemas.responses.party_read import PartyRead

class PartyServiceInterface(ABC):
    
    @abstractmethod
    def get_by_id(self, id_party: UUID) -> PartyRead:
        pass
    
    @abstractmethod
    def get_by_nit(self, nit: str) -> PartyRead:
        pass
    
    @abstractmethod
    def get_all(self) -> List[PartyRead]:
        pass
    
    @abstractmethod
    def get_by_type(self, party_type: str) -> List[PartyRead]:
        pass
    
    @abstractmethod 
    def search_by_name(self, name: str) -> List[PartyRead]:
        pass
    
    @abstractmethod
    def create_party(self, party_dto: PartyCreate) -> PartyRead:
        pass
    
    @abstractmethod
    def update_party(self, id_party: UUID, dto: PartyUpdate) -> PartyRead:
        pass
    
    @abstractmethod
    def delete_party(self, id_user: UUID):
        pass