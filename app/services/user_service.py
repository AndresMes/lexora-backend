from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.requests.user_request import UserRequest
from app.schemas.responses.user_read import UserRead
from app.services.interfaces.user_service_interface import UserServiceInterface

from app.utils.password_hasher import hash_password


class UserService(UserServiceInterface):
    
    def __init__(self, user_repo: UserRepository):    
        self.user_repo= user_repo
        
    def create_user(self, userDto):
        
        if self.user_repo.exists_by_email(userDto.email):
            raise HTTPException(status_code=409, detail="Email already exists")
        
        password_hash = hash_password(userDto.password)
        
        user = User(email=userDto.email.lower().strip(), password_hash=password_hash)
        
        saved_user = self.user_repo.create(user)
        
        return UserRead(
            id=saved_user.id,
            email=saved_user.email,
            created_at=saved_user.created_at
        )
        
    def get_user_by_id(self, id_user: UUID) -> UserRead:

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserRead(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )

    def get_by_email(self, email: str) -> UserRead:

        user = self.user_repo.get_by_email(email.lower().strip())

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserRead(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )

    def update_user(self, id_user: UUID, userDto: UserRequest) -> UserRead:

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        existing_user = self.user_repo.get_by_email(userDto.email)
        if existing_user and existing_user.id != id_user:
            raise HTTPException(status_code=409, detail="Email already in use")

        user.email = userDto.email.lower().strip()

        if userDto.password:
            user.password_hash = hash_password(userDto.password)

        updated_user = self.user_repo.update(user)

        return UserRead(
            id=updated_user.id,
            email=updated_user.email,
            created_at=updated_user.created_at
        )

    def delete_user(self, id_user: UUID):

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.user_repo.delete(id_user)

        return {"message": "User deleted successfully"}
        
    