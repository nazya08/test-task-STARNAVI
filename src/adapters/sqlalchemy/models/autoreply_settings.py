from datetime import timedelta

from sqlalchemy import Column, Integer, ForeignKey, Boolean, Interval
from sqlalchemy.orm import relationship

from src.adapters.sqlalchemy.db.base_class import Base


class AutoReplySettings(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    is_enabled = Column(Boolean, default=False)
    reply_delay = Column(Interval, default=timedelta(minutes=5))

    user = relationship("User", back_populates="auto_reply_settings")
