from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from src.adapters.schemas.post import PostResponse, PostCreate, PostUpdate, PostExternalResponse
from src.adapters.sqlalchemy.models import Post, User
from src.adapters.sqlalchemy.models.user import UserType
from src.presentation.dependencies.base import get_db
from src.presentation.dependencies.post import get_post, get_post_service
from src.presentation.dependencies.user import PermissionChecker, get_current_user, get_user, get_current_active_user
from src.services.post import PostFilter, PostService

router = APIRouter()

# allow_delete_resource = PermissionChecker(
#     [UserType.admin, UserType.default_user]
# )


@router.get("/")
def read_all_posts(
        filters: PostFilter = Depends(),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    """
    Retrieve paginated posts response.
    """
    return filters.filter_posts(db, skip, limit)


@router.get("/{post_id}", response_model=PostExternalResponse)
def read_post_by_id(
        post: Post = Depends(get_post),
        post_service: PostService = Depends(get_post_service)
):
    """
    Read a post by id.
    """
    count_of_comments = post_service.get_count_of_comments(post_id=post.id)
    post_detail = PostResponse(
        id=post.id,
        title=post.title,
        description=post.description,
        created_by_id=post.created_by_id,
        is_blocked=post.is_blocked,
        created_at=post.created_at,
        updated_at=post.updated_at
    )
    return PostExternalResponse(
        post_detail=post_detail,
        comments=count_of_comments
    )


@router.get("/user/{user_id}", response_model=List[PostResponse])
def read_user_posts(user: User = Depends(get_user)):
    """
    Read user posts by user_id.
    """
    return user.posts


@router.post("/")
def create_post(
        *,
        post_service: PostService = Depends(get_post_service),
        post_in: PostCreate,
        current_user: User = Depends(get_current_active_user)
):
    """
    Create a post.
    """
    post = post_service.create_post(obj_in=post_in, current_user=current_user)

    return PostResponse(
        id=post.id,
        title=post.title,
        description=post.description,
        created_by_id=current_user.id,
        is_blocked=post.is_blocked,
        created_at=post.created_at,
        updated_at=post.updated_at
    )


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_in: PostUpdate,
    post_service: PostService = Depends(get_post_service),
    post: Post = Depends(get_post),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a post.
    """
    updated_post = post_service.update_post(post=post, post_data=post_in, current_user=current_user)

    return PostResponse(
        id=updated_post.id,
        title=updated_post.title,
        description=updated_post.description,
        created_by_id=current_user.id,
        is_blocked=updated_post.is_blocked,
        created_at=updated_post.created_at,
        updated_at=updated_post.updated_at
    )


@router.delete("/{post_id}", status_code=HTTP_204_NO_CONTENT)
def remove_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a post.
    """
    return post_service.delete_post(post_id=post_id, current_user=current_user)
