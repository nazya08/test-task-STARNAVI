from abc import abstractmethod
from typing import Protocol

from src.adapters.sqlalchemy.models import AutoReplySettings


class AutoReplyReader(Protocol):
    @abstractmethod
    def get_settings_by_user_id(self, user_id: int) -> AutoReplySettings:
        raise NotImplementedError


class AutoReplySaver(Protocol):
    @abstractmethod
    def save_settings(self, settings: AutoReplySettings):
        raise NotImplementedError

    @abstractmethod
    def update_settings(self, settings: AutoReplySettings):
        raise NotImplementedError
