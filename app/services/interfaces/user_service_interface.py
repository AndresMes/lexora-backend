from abc import ABC, abstractmethod
from ast import List
from uuid import UUID

from app.schemas.requests.user_request import UserRequest
from app.schemas.responses.user_read import UserRead

class UserServiceInterface(ABC):
    
    @abstractmethod
    def create_user(self, userDto: UserRequest) -> UserRead:
        pass
    
    @abstractmethod
    def get_user_by_id(self, id_user: UUID) -> UserRead:
        pass
    
    @abstractmethod
    def update_user(self, id_user: UUID, userDto:UserRequest) -> UserRead