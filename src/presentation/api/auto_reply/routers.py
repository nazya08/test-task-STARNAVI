from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from src.adapters.sqlalchemy.models import User, Comment, Post
from src.presentation.dependencies.auto_reply import get_auto_reply_service
from src.presentation.dependencies.comment import get_comment
from src.presentation.dependencies.post import get_post
from src.presentation.dependencies.user import get_current_active_user
from src.services.auto_reply import AutoReplyService

router = APIRouter()


@router.post("/enable-auto-reply/")
def enable_auto_reply(
        delay: int,
        auto_reply_service: AutoReplyService = Depends(get_auto_reply_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Enable the auto-reply feature for the current user.
    """
    auto_reply_service.enable_auto_reply(current_user.id, timedelta(minutes=delay))
    return {"message": "Auto-reply enabled"}


@router.post("/disable-auto-reply/")
def disable_auto_reply(
        auto_reply_service: AutoReplyService = Depends(get_auto_reply_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Disable the auto-reply feature for the current user.
    """
    auto_reply_service.disable_auto_reply(current_user.id)
    return {"message": "Auto-reply disabled"}


@router.get("/auto-reply-settings/")
def get_auto_reply_settings(
        auto_reply_service: AutoReplyService = Depends(get_auto_reply_service),
        current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve the auto-reply settings for the current user.
    """
    settings = auto_reply_service.get_settings(current_user.id)
    if not settings:
        return {"is_enabled": False, "reply_delay": None}
    return {"is_enabled": settings.is_enabled, "reply_delay": settings.reply_delay.total_seconds() / 60}


@router.post("/schedule-auto-reply/")
def schedule_auto_reply(
        post: Post = Depends(get_post),
        comment: Comment = Depends(get_comment),
        auto_reply_service: AutoReplyService = Depends(get_auto_reply_service),
        current_user: User = Depends(get_current_active_user)
):
    """
        Schedule an auto-reply to a comment on a post.

        Args:
            post (Post): The post to which the comment belongs.
            comment (Comment): The comment that will receive the auto-reply.
            auto_reply_service (AutoReplyService): The service to handle auto-reply logic.
            current_user (User): The current authenticated user.

        Returns:
            dict: A success message indicating that the auto-reply has been scheduled.

        Raises:
            HTTPException: If an error occurs during the scheduling process.
        """
    try:
        auto_reply_service.create_auto_reply(post=post, comment=comment, user=current_user)
        return {"message": "Auto-reply scheduled"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling auto-reply: {e}")
