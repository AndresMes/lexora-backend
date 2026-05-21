
from app.auth.jwt_service import JWTService


def get_jwt_service() -> JWTService:
    return JWTService()