from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, lostItem, helpPost, action
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)

api_router.include_router(lostItem.router)
api_router.include_router(helpPost.router)
api_router.include_router(action.router_comment)
api_router.include_router(action.router_like)


