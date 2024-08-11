from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.adapters.repositories.post import PostDbGateway
from src.presentation.dependencies.base import get_db
from src.services.post import PostService


def get_post_db_gateway(db: Session = Depends(get_db)) -> PostDbGateway:
    return PostDbGateway(session=db)


def get_post_service(post_db_gateway: PostDbGateway = Depends(get_post_db_gateway)) -> PostService:
    return PostService(post_db_gateway=post_db_gateway)


def get_post(
        post_id: int,
        post_db_gateway: PostDbGateway = Depends(get_post_db_gateway)
):
    post = post_db_gateway.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post
