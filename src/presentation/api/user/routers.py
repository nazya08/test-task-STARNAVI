from typing import Any

from fastapi import APIRouter, Depends

from src.adapters.schemas.pagination import Pagination, PaginationResponse
from src.adapters.schemas.user import UserResponse, UserCreate, UserId, UsersListResponse, UserExtendedData, UserUpdate
from src.adapters.sqlalchemy.models import User
from src.presentation.dependencies.user import get_current_active_superuser, get_current_active_user, get_user_service
from src.services.user import UserService

router = APIRouter()


@router.get("/", response_model=UsersListResponse)
def read_users(
        skip: int = 0,
        limit: int = 10,
        user_service: UserService = Depends(get_user_service),
        current_superuser: User = Depends(get_current_active_superuser),
) -> UsersListResponse:
    """
    Retrieve paginated users response.
    """
    users = user_service.get_users_list(Pagination(skip=skip, limit=limit))
    total = user_service.user_db_gateway.get_users_total()

    return UsersListResponse(
        pagination_detail=PaginationResponse(
            skip=skip, limit=limit, total=total
        ),
        users_list=[
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                type=user.type,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
    )


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Get user by id.
    """
    user = user_service.get_user(UserId(id=user_id))

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        type=user.type,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.post("/", response_model=UserResponse)
def create_user(
        user_in: UserCreate,
        user_service: UserService = Depends(get_user_service),
        current_superuser: User = Depends(get_current_active_superuser)
) -> UserResponse:
    """
    Create new user.
    """

    user = user_service.create_user(obj_in=user_in)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        type=user.type,
        created_at=user.created_at,
        updated_at=user.updated_at
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserExtendedData,
    user_service: UserService = Depends(get_user_service),
    current_superuser: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Update a user.
    """
    user_update_data = UserUpdate(user_id=user_id, user_data=user_in)
    updated_user = user_service.update_user(data=user_update_data)

    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        is_active=updated_user.is_active,
        type=updated_user.type,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )
