from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import func, Integer

from src.adapters.repositories.common.comment import CommentReader, CommentSaver, CommentsReader
from src.adapters.sqlalchemy.db.session import SessionLocal
from src.adapters.sqlalchemy.models.comment import Comment


class CommentDbGateway(CommentReader, CommentsReader, CommentSaver):
    def __init__(self, session: SessionLocal):
        self.session = session

    def save_comment(self, comment: Comment) -> None:
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)

    def get_comment_by_post_id(self, post_id: int, comment_id: int) -> Optional[Comment]:
        return self.session.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.id == comment_id,
            Comment.is_blocked == False
        ).first()

    def get_comments_by_post_id(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        return self.session.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.is_blocked == False
        ).offset(skip).limit(limit).all()

    def delete_comment(self, post_id: int, comment_id: int) -> None:
        comment = self.get_comment_by_post_id(post_id, comment_id)
        if comment:
            self.session.delete(comment)
            self.session.commit()

    def get_comments_daily_breakdown(self, start_date: str, end_date: str, post_id: Optional[int] = None) -> List[dict]:
        query = self.session.query(
            func.date(Comment.created_at).label('date'),
            func.count(Comment.id).label('total_comments'),
            func.sum(Comment.is_blocked.cast(Integer)).label('blocked_comments')
        ).filter(
            Comment.created_at.between(start_date, end_date)
        )

        if post_id:
            query = query.filter(Comment.post_id == post_id)

        daily_stats = query.group_by(func.date(Comment.created_at)).all()

        return daily_stats
