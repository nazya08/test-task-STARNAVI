import re

from typing import Optional, Union, List

from src.adapters.repositories.auto_reply import auto_reply_db_gateway
from src.adapters.repositories.user import UserDbGateway
from src.adapters.schemas.pagination import Pagination
from src.adapters.schemas.user import UserCreate, UserSignUp, UserId, UserUpdate
from src.adapters.sqlalchemy.models import User, AutoReplySettings
from src.adapters.sqlalchemy.models.user import UserType
from src.main.security import verify_password, get_password_hash
from src.services.common.exceptions import WeakPasswordError, UserNotFoundError, UserExistsError


class UserService:

    def __init__(self, user_db_gateway: UserDbGateway) -> None:
        self.user_db_gateway = user_db_gateway

    def create_user(self, obj_in: Union[UserCreate, UserSignUp]) -> User:
        user_data = obj_in.dict()

        if self.user_db_gateway.get_user_by_username(user_data['username']):
            raise UserExistsError(status_code=400, detail="User with this username already exists.")

        if self.user_db_gateway.get_user_by_email(user_data['email']):
            raise UserExistsError(status_code=400, detail="User with this email already exists.")

        password = user_data.pop("password")
        response, msg = self.validate_password(password)
        if not response:
            raise WeakPasswordError(status_code=400, detail=msg)

        user_data["hashed_password"] = get_password_hash(password)
        user_db_obj = User(**user_data)

        self.user_db_gateway.save_user(user_db_obj)

        auto_reply_settings = AutoReplySettings(user_id=user_db_obj.id)
        auto_reply_db_gateway.save_settings(auto_reply_settings)

        return user_db_obj

    def update_user(self, data: UserUpdate):
        user = self.user_db_gateway.get_user_by_id(data.user_id)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found.")

        if self.user_db_gateway.get_user_by_username(data.user_data.username):
            raise UserExistsError(status_code=400, detail="User with this username already exists.")

        if self.user_db_gateway.get_user_by_email(data.user_data.email):
            raise UserExistsError(status_code=400, detail="User with this email already exists.")

        dict_data = data.user_data.dict()
        for field, value in dict_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        self.user_db_gateway.save_user(user)

        return user

    def get_users_list(self, data: Pagination) -> List[User]:
        return self.user_db_gateway.get_users_list(skip=data.skip, limit=data.limit)

    def get_users_total(self) -> int:
        return self.user_db_gateway.get_users_total()

    def get_user(self, data: UserId) -> User:
        user = self.user_db_gateway.get_user_by_id(data.id)
        if not user:
            raise UserNotFoundError(status_code=404, detail="User not found.")

        return user

    def sign_up(self, obj_in: UserSignUp) -> Optional[User]:
        # if self.user_db_gateway.get_user_by_email(obj_in.email):
        #     raise UserExistsError(status_code=400, detail="User with this email already exists.")

        user = self.create_user(obj_in)
        self.user_db_gateway.save_user(user)

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.user_db_gateway.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.type == UserType.admin

    def validate_password(self, password: str) -> tuple[bool, str]:  # TODO: relocate to another file
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[a-z]", password):
            return (
                False,
                "Password must contain at least one lowercase letter.",
            )
        if not re.search(r"[A-Z]", password):
            return (
                False,
                "Password must contain at least one uppercase letter.",
            )

        return True, "Password is valid"
