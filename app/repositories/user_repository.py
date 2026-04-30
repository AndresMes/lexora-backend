from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlmodel import Session, select
from ..models.user import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = (
            select(User)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

    def exists_by_email(self, email: str) -> bool:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first() is not None