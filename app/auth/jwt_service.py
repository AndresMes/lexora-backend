from datetime import datetime, timedelta
from uuid import UUID
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class JWTService():
    
    def create_access_token(self, id_user: UUID):
        
        exp = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        payload = {"sub" : str(id_user), "exp": exp}
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
        return token
        
    
    def decode_access_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id_user = payload.get("sub")
            return id_user
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        