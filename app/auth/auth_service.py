from typing import Optional

from fastapi import HTTPException

from app.auth.jwt_service import JWTService
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.password_hasher import verify_password


class AuthService():
    
    def __init__(self, user_repo: UserRepository, jwt_service: JWTService):
        self.user_repo = user_repo
        self.jwt_service = jwt_service
    
    def login(self, email:str, password: str):
        
        user: User = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=401)
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401)
        
        return self.jwt_service.create_access_token(user.id)
        
        
        
        
        