import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.action_model import CommentPublic, Comment, CommentCreate, CommentsPublic, Like

# Comment Routes
router_comment = APIRouter(prefix="/comments", tags=["comments"])
router_like = APIRouter(prefix="/likes", tags=["likes"])


@router_comment.post("/", response_model=CommentPublic)
def create_comment(session: SessionDep, current_user: CurrentUser, comment_in: CommentCreate) -> Any:
    comment = Comment.model_validate(comment_in, update={"user_id": current_user.id})
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router_comment.get("/by-post/{post_id}", response_model=CommentsPublic)
def get_comments_by_post(session: SessionDep, post_id: uuid.UUID) -> Any:
    comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
    return CommentsPublic(data=comments, count=len(comments))

# Like Routes

@router_like.post("/", response_model=Like)
def like_post(session: SessionDep, current_user: CurrentUser, like_in: Like) -> Any:
    like = Like.model_validate(like_in, update={"user_id": current_user.id})
    session.add(like)
    session.commit()
    session.refresh(like)
    return like

@router_like.get("/count/{post_id}", response_model=int)
def count_likes(session: SessionDep, post_id: uuid.UUID) -> int:
    return session.exec(select(func.count()).select_from(Like).where(Like.post_id == post_id)).one()
