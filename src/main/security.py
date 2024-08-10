from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.main.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.TOKEN_ALGORITHM


def create_token(
        secret_key: str, expire: datetime, sub: str, email: str
) -> str:
    to_encode = {"exp": expire, "sub": sub, "email": email}
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(user_id: int, user_email: str) -> str:
    expire = datetime.now() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return create_token(
        secret_key=settings.JWT_SECRET_KEY,
        expire=expire,
        sub=str(user_id),
        email=user_email,
    )


def create_refresh_token(user_id: int, user_email: str) -> str:
    expire = datetime.now() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    return create_token(
        secret_key=settings.JWT_REFRESH_SECRET_KEY,
        expire=expire,
        sub=str(user_id),
        email=user_email,
    )


def create_activation_token(user_id: int, user_email: str) -> str:
    expire = datetime.now() + timedelta(
        minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES
    )
    return create_token(
        secret_key=settings.ACTIVATION_SECRET_KEY,
        expire=expire,
        sub=str(user_id),
        email=user_email,
    )


def decode_token(token: str, secret_key: str) -> dict[str, str]:
    try:
        decoded_token = jwt.decode(
            token=token, key=secret_key, algorithms=[ALGORITHM]
        )
        exp_datetime = datetime.fromtimestamp(
            decoded_token["exp"], timezone.utc
        )
        print(exp_datetime)
        return (
            decoded_token
            if exp_datetime >= datetime.now(timezone.utc)
            else None
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:

        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )


def decode_access_token(token: str) -> dict[str, str]:
    return decode_token(token=token, secret_key=settings.JWT_SECRET_KEY)


def decode_refresh_token(token: str) -> dict[str, str]:
    return decode_token(
        token=token, secret_key=settings.JWT_REFRESH_SECRET_KEY
    )


def decode_activation_token(token: str) -> dict[str, str]:
    return decode_token(token=token, secret_key=settings.ACTIVATION_SECRET_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
