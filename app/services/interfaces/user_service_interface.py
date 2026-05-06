from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.requests.user_create import UserCreate
from app.schemas.requests.user_update import UserUpdate
from app.schemas.responses.user_read import UserRead

class UserServiceInterface(ABC):
    
    @abstractmethod
    def create_user(self, userDto: UserCreate) -> UserRead:
        pass
    
    @abstractmethod
    def get_user_by_id(self, id_user: UUID) -> UserRead:
        pass
    
    @abstractmethod
    def get_by_email(self, email:str) -> UserRead:
        pass
    
    @abstractmethod
    def update_user(self, id_user: UUID, userDto:UserUpdate) -> UserRead:
        pass
    
    @abstractmethod
    def delete_user(self, id_user: UUID):
        pass