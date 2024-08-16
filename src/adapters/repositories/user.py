from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError

from src.adapters.repositories.common.user import UserReader, UsersReader, UserSaver
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models import AutoReplySettings
from src.adapters.sqlalchemy.models.user import User


class UserDbGateway(UserReader, UsersReader, UserSaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def save_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

    def create_user(self, user: User) -> User:
        try:
            self.save_user(user)
            auto_reply_settings = AutoReplySettings(user_id=user.id)
            self.session.add(auto_reply_settings)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e

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
