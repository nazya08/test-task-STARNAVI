from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base
from src.adapters.sqlalchemy.models.base import TimestampedModel


class Comment(Base, TimestampedModel):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    is_blocked = Column(Boolean, default=False)

    post = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")
