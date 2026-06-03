from fastapi import HTTPException

from app.auth.jwt_service import JWTService
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.requests.user_create import UserCreate
from app.utils.password_hasher import hash_password, verify_password
from app.schemas.responses.user_read import UserRead


class AuthService():
    
    def __init__(self, user_repo: UserRepository, jwt_service: JWTService):
        self.user_repo = user_repo
        self.jwt_service = jwt_service
    
    def login(self, email:str, password: str) -> dict:
        
        user: User = self.user_repo.get_by_email(email)
        
        if not user:
            raise HTTPException(status_code=401,  detail="Credenciales inválidas")
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        token = self.jwt_service.create_access_token(user.id)
        
        return {
            "user": UserRead(
                id=user.id,
                name=user.name,
                email=user.email,
                created_at=user.created_at
            ),
            "access_token": token,
            "token_type": "bearer",
        }
    
    def register(self, userDto: UserCreate) -> dict:

        # Validar que el email no exista
        if self.user_repo.exists_by_email(userDto.email):
            raise HTTPException(status_code=409, detail="El email ingresado ya existe")
        
        password_hash = hash_password(userDto.password)
        
        # Crear usuario
        user = User(
            name=userDto.name, 
            email=userDto.email.lower().strip(), 
            password_hash=password_hash
        )
        
        saved_user = self.user_repo.create(user)
        
        # Generar token
        token = self.jwt_service.create_access_token(saved_user.id)
        
        # Retornar respuesta
        return {
            "user": UserRead(
                id=saved_user.id,
                name=saved_user.name,
                email=saved_user.email,
                created_at=saved_user.created_at
            ),
            "access_token": token,
            "token_type": "bearer",
        }  