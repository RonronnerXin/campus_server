import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep, CurrentUser
from app.models.helpPost_model import HelpPostsPublic, HelpPost, HelpPostPublic, HelpPostCreate

router = APIRouter(prefix="/help-posts", tags=["help_posts"])

@router.get("/", response_model=HelpPostsPublic)
def read_help_posts(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    posts = session.exec(select(HelpPost).offset(skip).limit(limit)).all()
    count = session.exec(select(func.count()).select_from(HelpPost)).one()
    return HelpPostsPublic(data=posts, count=count)

@router.post("/", response_model=HelpPostPublic)
def create_help_post(session: SessionDep, current_user: CurrentUser, post_in: HelpPostCreate) -> Any:
    post = HelpPost.model_validate(post_in, update={"user_id": current_user.id})
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/{id}", response_model=HelpPostPublic)
def get_help_post(session: SessionDep, id: uuid.UUID) -> Any:
    post = session.get(HelpPost, id)
    if not post:
        raise HTTPException(status_code=404, detail="Help post not found")
    return post
