from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]