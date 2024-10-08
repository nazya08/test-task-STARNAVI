from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.comment import CommentCreate, CommentUpdate
from src.adapters.sqlalchemy.models import Post, Comment, User
from src.presentation.dependencies.auto_reply import get_auto_reply_service
from src.presentation.dependencies.comment import get_comment_service, get_comment, check_comment_access
from src.presentation.dependencies.post import get_post
from src.presentation.dependencies.user import get_current_active_user
from src.services.auto_reply import AutoReplyService
from src.services.comment import CommentService

router = APIRouter()


@router.get("/{post_id}/comments/")
def read_all_comments(
        post: Post = Depends(get_post),
        comment_service: CommentService = Depends(get_comment_service),
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve comments by post_id.
    """
    comments = comment_service.get_list_by_post_id(post_id=post.id, skip=skip, limit=limit)
    return comments


@router.get("/{post_id}/comments/{comment_id}")
def read_comment_by_id(
        post: Post = Depends(get_post), comment: Comment = Depends(get_comment)
):
    """
    Read a comment by id.
    """
    return comment


@router.post("/{post_id}/comments/")
def create_comment(
        *,
        post: Post = Depends(get_post),
        comment_in: CommentCreate,
        comment_service: CommentService = Depends(get_comment_service),
        current_user: User = Depends(get_current_active_user),
        auto_reply_service: AutoReplyService = Depends(get_auto_reply_service)
):
    """
    Create a comment.
    """
    comment = comment_service.create_comment_with_check(post_id=post.id, obj_in=comment_in, current_user=current_user)
    # Call the method to create an automatic reply
    if not comment.is_blocked:
        if post.created_by.id != current_user.id and post.created_by.auto_reply_settings.is_enabled:
            auto_reply_service.create_delayed_auto_reply(post=post, comment=comment)

    return comment


@router.patch("/{post_id}/comments/{comment_id}")
def update_comment(
        *,
        post: Post = Depends(get_post),
        comment: Comment = Depends(get_comment),
        comment_in: CommentUpdate,
        comment_access: None = Depends(check_comment_access),
        comment_service: CommentService = Depends(get_comment_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Update a comment.
    """
    comment = comment_service.update_comment(db_obj=comment, obj_in=comment_in)
    return comment


@router.delete("/{post_id}/comments/{comment_id}", status_code=HTTP_204_NO_CONTENT)
def remove_comment(
        *,
        post: Post = Depends(get_post),
        comment: Comment = Depends(get_comment),
        comment_access: None = Depends(check_comment_access),
        comment_service: CommentService = Depends(get_comment_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Delete a comment.
    """
    return comment_service.remove_comment(post_id=post.id, comment_id=comment.id)


@router.get("/comments/daily_breakdown/")
def comments_daily_breakdown(
        *,
        start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
        end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
        post_id: Optional[int] = Query(None, description="Filter by post ID"),
        post: Post = Depends(get_post),
        comment_service: CommentService = Depends(get_comment_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Get the daily breakdown of comments within a specified date range.
    """
    return comment_service.get_comments_daily_breakdown(start_date, end_date, post_id)
