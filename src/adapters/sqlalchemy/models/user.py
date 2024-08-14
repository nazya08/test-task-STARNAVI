from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel


class UserType(PyEnum):
    default_user = "default_user"
    admin = "admin"


class User(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    type = Column(Enum(UserType), default=UserType.default_user)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="created_by")
    comments = relationship("Comment", back_populates="owner")
    auto_reply_settings = relationship("AutoReplySettings", uselist=False, back_populates="user")
