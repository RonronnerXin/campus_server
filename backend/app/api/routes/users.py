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

router = APIRouter(prefix="/users", tags=["users"])

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

@router.post("/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="密码错误")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="新密码不能和旧密码相同"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="密码修改成功")

@router.get("/getValidateCode")
async def get_captcha():
    # 调用验证码生成服务
    base64_img, result = await CaptchaService.create_captcha_image_service()
    return {
        "img": base64_img,  # 前端展示的图片Base64
        "validateCodeId": str(result)  # 后端保存的正确结果，用于后续验证
    }


@router.post("/testValidateInfo")
async def validate_code(request: ValidateRequest):
    if request.validate_code_id == request.validate_code:
        is_valid = True
    else:
        is_valid = False
    return {
        "code": 0 if is_valid else 400,
        "msg": "验证成功" if is_valid else "验证码错误或已过期"
    }


@router.post("/getEmailCode")
async def send_email_code(request: EmailCodeRequest):
    # 生成并存储验证码
    code = EmailCodeService.generate_code()
    EmailCodeService.store_code(request.email, code)

    # 清理过期验证码
    EmailCodeService.cleanup_expired()

    # 发送邮件
    email_data = generate_email_code_template(email_to=request.email, code=code)
    try:
        send_email(
            email_to=request.email,
            subject=email_data.subject,
            html_content=email_data.html_content
        )
    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")
        raise HTTPException(503, detail=str(e))

    return {"code": 0}

@router.post("/verifyEmailCode")
async def verify_email_code(request: EmailValidateRequest):
    if not EmailCodeService.validate_code(request.email, request.validateCode):
        raise HTTPException(400, "验证码错误或已过期")
    return {"message": "验证成功"}

@router.get("/")
def get_user(current_user: CurrentUser):
    return current_user


