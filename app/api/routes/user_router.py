from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.user_service_dep import get_user_service
from app.auth.dependencies import get_current_user
from app.models.user import User
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


@user_router.get("/me", response_model=UserRead)
def get_profile(
    service: UserServiceInterface = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    
    return service.get_user_by_id(current_user.id)



@user_router.put("/me", response_model=UserRead)
def update_user(
    userDto: UserUpdate,
    service: UserServiceInterface = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return service.update_user(current_user.id, userDto)


@user_router.delete("/me")
def delete_user(
    service: UserServiceInterface = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return service.delete_user(current_user.id)