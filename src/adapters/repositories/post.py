from typing import List, Optional

from src.adapters.repositories.common.post import PostReader, PostSaver, PostsReader
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models import Comment
from src.adapters.sqlalchemy.models.post import Post


class PostDbGateway(PostReader, PostsReader, PostSaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def save_post(self, post: Post) -> None:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)

    def get_post_by_id(self, id: int) -> Optional[Post]:
        return self.session.query(Post).filter(Post.id == id).first()

    def get_user_posts(self, user_id: int) -> List[Post]:
        return self.session.query(Post).filter_by(created_by_id=user_id).all()

    def get_posts_list(self, skip: int, limit: int) -> List[Post]:
        return self.session.query(Post).offset(skip).limit(limit).all()

    def get_count_comments_by_post_id(self, post_id: int) -> int:
        return self.session.query(Comment).filter(Comment.post_id == post_id).count()

    def update_post(self, post_id: int, post_data: dict) -> Optional[Post]:
        post = self.get_post_by_id(post_id)
        if not post:
            return None
        for key, value in post_data.items():
            setattr(post, key, value)

        self.session.commit()
        self.session.refresh(post)

        return post

    def delete_post(self, post_id: int) -> None:
        post = self.get_post_by_id(post_id)
        if post:
            self.session.delete(post)
            self.session.commit()
