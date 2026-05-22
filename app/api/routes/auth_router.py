from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.auth_service_dep import get_auth_service
from app.auth.auth_service import AuthService



auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
    ):
    
    token = service.login(email=form_data.username, password=form_data.password)
    return {"access_token": token, "token_type": "bearer"}