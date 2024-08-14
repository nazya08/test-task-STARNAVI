from fastapi import APIRouter
from src.presentation.api.auth import routers as auth_routers
from src.presentation.api.user import routers as user_routers
from src.presentation.api.post import routers as post_routers
from src.presentation.api.comment import routers as comment_routers
from src.presentation.api.auto_reply import routers as auto_reply_routers

api_router = APIRouter()

api_router.include_router(auth_routers.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routers.router, prefix="/users", tags=["user"])
api_router.include_router(post_routers.router, prefix="/posts", tags=["post"])
api_router.include_router(comment_routers.router, prefix="/posts", tags=["comment"])
api_router.include_router(auto_reply_routers.router, prefix="/comments", tags=["auto_reply"])


@api_router.get("/alive")
def alive():
    return {'status': 'ok'}
