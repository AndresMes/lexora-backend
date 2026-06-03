from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.auth_service_dep import get_auth_service
from app.schemas.requests.user_create import UserCreate
from app.schemas.responses.auth_response import AuthResponse

from app.auth.auth_service import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login", response_model=AuthResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
    ):
    
    return service.login(email=form_data.username, password=form_data.password)

@auth_router.post("/register", response_model=AuthResponse)
def register(
    userDto: UserCreate,
    service: AuthService = Depends(get_auth_service)
    ):
    
    return service.register(userDto)