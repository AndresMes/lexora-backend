from fastapi import Depends

from app.api.deps.jwt_service_dep import get_jwt_service
from app.api.deps.repo_deps import get_user_repo
from app.auth.auth_service import AuthService
from app.auth.jwt_service import JWTService
from app.repositories.user_repository import UserRepository


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> AuthService:
    
    return AuthService(
        user_repo=user_repo,
        jwt_service=jwt_service
    )