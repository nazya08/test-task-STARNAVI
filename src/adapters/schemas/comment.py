from typing import Optional

from pydantic import BaseModel


class BaseComment(BaseModel):
    content: Optional[str]


class CommentCreate(BaseComment):
    pass


class CommentUpdate(BaseComment):
    pass
