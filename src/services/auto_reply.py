from datetime import timedelta

from fastapi import HTTPException

from src.adapters.repositories.auto_reply import AutoReplyDbGateway
from src.adapters.sqlalchemy.models import AutoReplySettings, User, Comment, Post
from src.services.celery import celery_service
from src.services.open_ai import open_ai_service


class AutoReplyService:
    def __init__(self, auto_reply_db_gateway: AutoReplyDbGateway) -> None:
        self.auto_reply_db_gateway = auto_reply_db_gateway
        self.open_ai_service = open_ai_service
        self.celery_service = celery_service

    def enable_auto_reply(self, user_id: int, delay: timedelta) -> None:
        settings = self.auto_reply_db_gateway.get_settings_by_user_id(user_id)
        if not settings:
            settings = AutoReplySettings(user_id=user_id, is_enabled=True, reply_delay=delay)
            self.auto_reply_db_gateway.save_settings(settings)
        else:
            settings.is_enabled = True
            settings.reply_delay = delay
            self.auto_reply_db_gateway.update_settings(settings)

    def disable_auto_reply(self, user_id: int) -> None:
        settings = self.auto_reply_db_gateway.get_settings_by_user_id(user_id)
        if settings:
            settings.is_enabled = False
            self.auto_reply_db_gateway.update_settings(settings)

    def get_settings(self, user_id: int) -> AutoReplySettings:
        return self.auto_reply_db_gateway.get_settings_by_user_id(user_id)

    def create_auto_reply(self, post: Post, comment: Comment, user: User):
        settings = self.get_settings(user.id)
        if not settings or not settings.is_enabled:
            raise HTTPException(status_code=400, detail="Auto-reply is not enabled for the current user.")

        if post.created_by_id != user.id:
            raise HTTPException(status_code=403, detail="You are not the owner of this post")

        if comment.reply_to_comment_id is not None:
            raise HTTPException(status_code=400, detail="Auto-reply cannot be generated for replies to other comments.")

        reply_content = self.open_ai_service.generate_reply(post_content=post.description, comment_content=comment.content)
        auto_reply = {
            "content": reply_content,
            "post_id": post.id,
            "owner_id": user.id,
            "reply_to_comment_id": comment.id
        }

        self.celery_service.schedule_auto_reply(auto_reply, settings.reply_delay)
