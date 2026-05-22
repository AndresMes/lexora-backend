from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str = Field(nullable=False, max_length=250)
    email: str = Field(nullable=False, max_length=250, unique=True)
    password_hash: str = Field(nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)