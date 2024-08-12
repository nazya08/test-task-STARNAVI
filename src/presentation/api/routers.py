from fastapi import APIRouter
from src.presentation.api.auth import routers as auth_routes
from src.presentation.api.user import routers as user_routes
from src.presentation.api.post import routers as post_routes
from src.presentation.api.comment import routers as comment_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routes.router, prefix="/users", tags=["user"])
api_router.include_router(post_routes.router, prefix="/posts", tags=["post"])
api_router.include_router(comment_routes.router, prefix="/posts", tags=["comment"])


@api_router.get("/alive")
def alive():
    return {'status': 'ok'}
