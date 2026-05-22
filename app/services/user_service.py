from datetime import datetime
from uuid import UUID

from fastapi import HTTPException

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.requests.user_update import UserUpdate
from app.schemas.responses.user_read import UserRead
from app.services.interfaces.user_service_interface import UserServiceInterface

from app.utils.password_hasher import hash_password


class UserService(UserServiceInterface):
    
    def __init__(self, user_repo: UserRepository):    
        self.user_repo= user_repo
        
    def create_user(self, userDto):
        
        if self.user_repo.exists_by_email(userDto.email):
            raise HTTPException(status_code=409, detail="El email ingresado ya existe")
        
        password_hash = hash_password(userDto.password)
        
        user = User(name=userDto.name, email=userDto.email.lower().strip(), password_hash=password_hash)
        
        saved_user = self.user_repo.create(user)
        
        return UserRead(
            id=saved_user.id,
            name=saved_user.name,
            email=saved_user.email,
            created_at=saved_user.created_at
        )
        
    def get_user_by_id(self, id_user: UUID) -> UserRead:

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return UserRead(
            id=user.id,
            name = user.name,
            email=user.email,
            created_at=user.created_at
        )

    def get_by_email(self, email: str) -> UserRead:

        user = self.user_repo.get_by_email(email.lower().strip())

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return UserRead(
            id=user.id,
            name = user.name,
            email=user.email,
            created_at=user.created_at
        )

    def update_user(self, id_user: UUID, userDto: UserUpdate) -> UserRead:

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        existing_user = self.user_repo.get_by_email(userDto.email)
        if existing_user and existing_user.id != id_user:
            raise HTTPException(status_code=409, detail="El email ingresado ya está en uso")

        user.email = userDto.email.lower().strip()
        user.name = userDto.name.lower()

        if userDto.password:
            user.password_hash = hash_password(userDto.password)

        updated_user = self.user_repo.update_user(user)

        return UserRead(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            created_at=updated_user.created_at
        )

    def delete_user(self, id_user: UUID):

        user = self.user_repo.get_by_id(id_user)

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        self.user_repo.delete(user)

        return {"message": "Usuario eliminado satisfactoriamente"}
        
    