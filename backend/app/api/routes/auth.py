from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_limiter.depends import RateLimiter  # 需要安装依赖

from pydantic import EmailStr
from sqlmodel import Session
from typing import Any, Annotated

from app.api.deps import (
    get_db,
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core import security
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.crud import create_user, authenticate_user, get_user_by_email
from app.models.user_model import UserCreate, UserLogin, UserRegister, Token, ValidateRequest, EmailCodeRequest, \
    EmailValidateRequest, Message, UpdatePassword, UserToken
from app.utils import CaptchaService, EmailCodeService, generate_email_code_template, send_email, logger

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register_user(user_in: UserRegister, session: Session = Depends(get_db)) -> Any:
    user = get_user_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    user = create_user(session=session, user_create=user_in)
    return user

@router.post("/login")
def login_user(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> UserToken:
    user = authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="用户账号或密码错误")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return UserToken(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        user_id=user.id,
        username=user.username,
        avatar=user.avatar or ""  # 头像路径，若无则返回空字符串
    )
