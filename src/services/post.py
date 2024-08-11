from datetime import datetime
from typing import Optional, Union, List, Dict

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi_filter.contrib.sqlalchemy import Filter

from src.adapters.schemas.post import PostCreate, PostUpdate
from src.adapters.sqlalchemy.models import Post, User
from src.adapters.repositories.post import PostDbGateway
from src.adapters.sqlalchemy.models.user import UserType


class PostService:

    def __init__(self, post_db_gateway: PostDbGateway) -> None:
        self.post_db_gateway = post_db_gateway

    def create_post(self, obj_in: PostCreate, current_user: User) -> Post:
        if not current_user:
            raise HTTPException(status_code=400, detail="Invalid current user")

        post_data = obj_in.dict()
        post_data["created_by_id"] = current_user.id
        post_data["created_at"] = datetime.utcnow()

        post_db_obj = Post(**post_data)
        self.post_db_gateway.save_post(post_db_obj)

        return post_db_obj

    def update_post(self, post: Post, post_data: PostUpdate, current_user: User) -> Post:
        if post.created_by_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="You do not have permission to perform this action"
            )

        updated_post = self.post_db_gateway.update_post(post.id, post_data.dict())

        return updated_post

    def delete_post(self, post_id: int, current_user: User) -> None:
        post = self.post_db_gateway.get_post_by_id(post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.created_by_id != current_user.id and current_user.type != UserType.admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to delete this post"
            )

        self.post_db_gateway.delete_post(post_id)


class PostFilter(Filter):
    title: Optional[str] = None
    description: Optional[str] = None
    is_blocked: Optional[bool] = None

    class Constants(Filter.Constants):
        model = Post
        ordering_field_name = "order_by"
        search_field_name = "search"

    def filter_posts(
            self, db: Session, skip: int, limit: int
    ) -> Union[List[Post], Dict[str, str]]:
        """
        Filters and retrieves posts based on the provided filter parameters.

        Args:
            db: SQLAlchemy Session object for database access.
            skip: The number of posts to skip before returning results (pagination).
            limit: The maximum number of posts to return.

        Returns:
            A list of `Post` objects if the filtering is successful, or a dictionary
            containing an error message if any errors occur.

        Raises:
            SQLAlchemyError: If any database-related error occurs during the filtering process.

        """

        try:
            query = db.query(Post)

            if self.title:
                query = query.filter(Post.title.ilike(f"%{self.title}%"))
            if self.description:
                query = query.filter(
                    Post.description.ilike(f"%{self.description}%")
                )

            if self.is_blocked is not None:
                query = query.filter(Post.is_blocked == self.is_blocked)

            posts = query.offset(skip).limit(limit).all()
            return posts

        except SQLAlchemyError as e:
            return {"error": str(e)}
