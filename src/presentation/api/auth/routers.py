from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.adapters.schemas.token import TokensResponse, RefreshToken, RefreshTokenResponse
from src.adapters.schemas.user import UserLogin, SignUpResponse, UserSignUp, UserResponse
from src.adapters.sqlalchemy.models import User
from src.main.security import create_access_token, create_refresh_token, decode_refresh_token
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.user import get_user_service
from src.services.user import UserService

router = APIRouter()


@router.post("/login", response_model=TokensResponse)
def login_access_token(
        user_data: UserLogin = Body(...),
        user_service: UserService = Depends(get_user_service),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = user_service.authenticate(
        email=user_data.email, password=user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    elif not user_service.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(user_id=user.id, user_email=user.email)
    refresh_token = create_refresh_token(
        user_id=user.id, user_email=user.email
    )
    return TokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/sign-up", response_model=SignUpResponse)
def sign_up(
    user_in: UserSignUp,
    user_service: UserService = Depends(get_user_service),
) -> Any:
    """
    Sign Up as a new user.
    """

    user = user_service.sign_up(user_in)

    tokens = TokensResponse(
        access_token=create_access_token(
            user_id=user.id, user_email=user.email
        ),
        refresh_token=create_refresh_token(
            user_id=user.id, user_email=user.email
        ),
        token_type="bearer",
    )
    user_detail = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        type=user.type,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    print(tokens)
    print(user_detail)
    return SignUpResponse(user_detail=user_detail, tokens=tokens)


@router.post("/token-refresh", response_model=RefreshTokenResponse)
def token_refresh(
    token: RefreshToken, db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Refresh access token by the refresh token
    """
    payload = decode_refresh_token(token.refresh_token)

    user_id = payload.get("sub", None)
    user_email = payload.get("email", None)
    if not user_id or not user_email:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token.")

    user = (
        db.query(User)
        .filter(and_(User.id == int(user_id), User.email == user_email))
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail=f"The user belonging to this token no logger exist",
        )

    access_token = create_access_token(user_id=user.id, user_email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
