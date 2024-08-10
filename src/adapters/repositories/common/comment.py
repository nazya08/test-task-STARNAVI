from abc import abstractmethod
from typing import Protocol, Optional, List

from src.adapters.sqlalchemy.models.comment import Comment


class CommentReader(Protocol):
    @abstractmethod
    def get_comment_by_post_id(self, post_id: int, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError


class CommentsReader(Protocol):
    @abstractmethod
    def get_comments_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        raise NotImplementedError


class CommentSaver(Protocol):
    @abstractmethod
    def save_comment(self, post_id: int, comment_data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_comment(self, post_id: int, comment_id: int, comment_data: dict) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def delete_comment(self, post_id: int, comment_id: int) -> None:
        raise NotImplementedError
