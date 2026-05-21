
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.deps.jwt_service_dep import get_jwt_service
from app.api.deps.repo_deps import get_user_repo
from app.auth.jwt_service import JWTService
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    
async def get_current_user(token: str = Depends(oauth2_scheme), jwt_service: JWTService = Depends(get_jwt_service), user_repo: UserRepository = Depends(get_user_repo)):
    
    id_user = jwt_service.decode_access_token(token)
    user = user_repo.get_by_id(id_user)
    
    if not user:
        raise HTTPException(status_code=401, detail=f'Usuario no encontrado')
    
    return user