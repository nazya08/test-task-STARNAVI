from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel


class Post(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_blocked = Column(Boolean, default=False)

    created_by = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
