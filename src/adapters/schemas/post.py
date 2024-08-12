from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BasePost(BaseModel):
    title: Optional[str]
    description: Optional[str]


class PostResponse(BasePost):
    id: int
    created_by_id: int
    is_blocked: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostExternalResponse(BaseModel):
    post_detail: PostResponse
    comments: int


class PostCreate(BasePost):
    pass


class PostUpdate(BasePost):
    pass
