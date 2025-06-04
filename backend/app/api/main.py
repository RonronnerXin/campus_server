from fastapi import APIRouter

from app.api.routes import users, lostItem, blog, auth
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(users.router)

api_router.include_router(lostItem.router)
api_router.include_router(blog.router)
api_router.include_router(auth.router)



