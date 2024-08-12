from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.repositories.comment import CommentDbGateway
from src.adapters.sqlalchemy.models import Comment, User
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.user import get_current_user
from src.services.comment import CommentService


def get_comment_db_gateway(db: Session = Depends(get_db)) -> CommentDbGateway:
    return CommentDbGateway(session=db)


def get_comment_service(comment_db_gateway: CommentDbGateway = Depends(get_comment_db_gateway)) -> CommentService:
    return CommentService(comment_db_gateway=comment_db_gateway)


def get_comment(post_id: int, comment_id: int, comment_db_gateway: CommentDbGateway = Depends(get_comment_db_gateway)):
    comment = comment_db_gateway.get_comment_by_post_id(post_id=post_id, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    return comment


def check_comment_access(
        comment: Comment = Depends(get_comment),
        current_user: User = Depends(get_current_user),
):
    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission for this comment"
        )
