from typing import List

from fastapi import HTTPException

from src.adapters.repositories.comment import CommentDbGateway
from src.adapters.schemas.comment import CommentCreate, CommentUpdate
from src.adapters.sqlalchemy.models import Comment, User


class CommentService:
    def __init__(self, comment_db_gateway: CommentDbGateway) -> None:
        self.comment_db_gateway = comment_db_gateway

    def get_list_by_post_id(self,  post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        return self.comment_db_gateway.get_comments_by_post_id(post_id=post_id, skip=skip, limit=limit)

    def create_comment(self, post_id: int, obj_in: CommentCreate, current_user: User) -> Comment:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")

        comment_data = obj_in.dict()
        comment_data["post_id"] = post_id
        comment_data["owner_id"] = current_user.id

        comment_db_obj = Comment(**comment_data)
        self.comment_db_gateway.save_comment(comment_db_obj)

        return comment_db_obj

    def update_comment(self, db_obj: Comment, obj_in: CommentUpdate) -> Comment:
        update_data = obj_in.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.comment_db_gateway.save_comment(db_obj)
        return db_obj

    def remove_comment(self, post_id: int, comment_id: int):
        self.comment_db_gateway.delete_comment(post_id=post_id, comment_id=comment_id)
