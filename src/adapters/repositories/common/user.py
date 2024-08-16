from abc import abstractmethod
from typing import Protocol, List

from src.adapters.sqlalchemy.models.user import User


class UserSaver(Protocol):
    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError


class UserReader(Protocol):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> User:
        raise NotImplementedError


class UsersReader(Protocol):
    @abstractmethod
    def get_users_list(self, skip: int, limit: int) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_users_total(self) -> int:
        raise NotImplementedError
