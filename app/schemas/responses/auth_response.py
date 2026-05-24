from pydantic import BaseModel

from app.schemas.responses.user_read import UserRead

class AuthResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str
    