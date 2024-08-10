from typing import List, Optional

from src.adapters.repositories.common.user import UserReader, UsersReader, UserSaver
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models.user import User


class UserDbGateway(UserReader, UsersReader, UserSaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def save_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def get_user_by_id(self, id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_users_list(self, skip: int, limit: int) -> List[User]:
        return self.session.query(User).offset(skip).limit(limit).all()

    def get_users_total(self) -> int:
        return self.session.query(User).count()
