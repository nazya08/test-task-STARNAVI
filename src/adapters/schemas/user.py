from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from src.adapters.schemas.pagination import PaginationResponse
from src.adapters.schemas.token import TokensResponse
from src.adapters.sqlalchemy.models.user import UserType


class UserBaseData(BaseModel):
    username: str


class UserExtendedData(UserBaseData):
    email: EmailStr
    type: Optional[UserType] = UserType.default_user
    is_active: bool = True


class UserId(BaseModel):
    id: int


class UserResponse(UserExtendedData):
    id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSignUp(UserBaseData):
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    user_detail: UserResponse
    tokens: TokensResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserExtendedData):
    password: str


class UserUpdate(BaseModel):
    user_data: UserExtendedData
    user_id: int


class UsersListResponse(BaseModel):
    pagination_detail: PaginationResponse
    users_list: List[UserResponse]
