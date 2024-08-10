from abc import abstractmethod
from typing import Protocol, List, Optional

from src.adapters.sqlalchemy.models.post import Post


class PostReader(Protocol):
    @abstractmethod
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        raise NotImplementedError


class PostsReader(Protocol):
    @abstractmethod
    def get_user_posts(self, user_id: int) -> List[Post]:
        raise NotImplementedError

    @abstractmethod
    def get_posts_list(self, skip: int, limit: int) -> List[Post]:
        raise NotImplementedError


class PostSaver(Protocol):
    @abstractmethod
    def save_post(self, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id: int, post_data: dict) -> Post:
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id: int) -> None:
        raise NotImplementedError
