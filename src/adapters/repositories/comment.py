from typing import Optional, List

from src.adapters.repositories.common.comment import CommentReader, CommentSaver, CommentsReader
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models.comment import Comment


class CommentDbGateway(CommentReader, CommentsReader, CommentSaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def get_comment_by_post_id(self, post_id: int, comment_id: int) -> Optional[Comment]:
        return self.session.query(Comment).filter(Comment.post_id == post_id, Comment.id == comment_id).first()

    def get_comments_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        return self.session.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

    def save_comment(self, post_id: int, comment_data: dict) -> None:  # TODO
        comment = Comment(**comment_data, post_id=post_id)
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

    def update_comment(self, post_id: int, comment_id: int, comment_data: dict) -> Optional[Comment]:
        comment = self.get_comment_by_post_id(post_id, comment_id)
        if comment:
            for key, value in comment_data.items():
                setattr(comment, key, value)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def delete_comment(self, post_id: int, comment_id: int) -> None:
        comment = self.get_comment_by_post_id(post_id, comment_id)
        if comment:
            self.session.delete(comment)
            self.session.commit()
