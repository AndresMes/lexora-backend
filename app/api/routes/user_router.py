
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps.user_service_dep import get_user_service
from app.schemas.requests.user_create import UserCreate
from app.schemas.requests.user_update import UserUpdate
from app.schemas.responses.user_read import UserRead
from app.services.interfaces.user_service_interface import UserServiceInterface


user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/", response_model=UserRead)
def create_user(
    userDto: UserCreate,
    service: UserServiceInterface = Depends(get_user_service)
):
    return service.create_user(userDto)


@user_router.get("/{id_user}", response_model=UserRead)
def get_user_by_id(
    id_user: UUID,
    service: UserServiceInterface = Depends(get_user_service)
):
    return service.get_user_by_id(id_user)


@user_router.get("/by-email/{email}", response_model=UserRead)
def get_by_email(
    email: str,
    service: UserServiceInterface = Depends(get_user_service)
):
    return service.get_by_email(email)


@user_router.put("/{id_user}", response_model=UserRead)
def update_user(
    id_user: UUID,
    userDto: UserUpdate,
    service: UserServiceInterface = Depends(get_user_service)
):
    return service.update_user(id_user, userDto)


@user_router.delete("/{id_user}")
def delete_user(
    id_user: UUID,
    service: UserServiceInterface = Depends(get_user_service)
):
    return service.delete_user(id_user)