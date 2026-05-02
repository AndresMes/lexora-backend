from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.api.deps.repo_deps import get_user_repo
from app.services.interfaces.user_service_interface import UserServiceInterface
from app.services.user_service import UserService



def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserServiceInterface:

    return UserService(
        user_repo=user_repo
    )