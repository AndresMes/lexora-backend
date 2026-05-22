from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]