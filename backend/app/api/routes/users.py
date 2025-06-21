import os
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_limiter.depends import RateLimiter  # 需要安装依赖

from pydantic import EmailStr
from sqlmodel import Session
from typing import Any, Annotated, Dict

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
    EmailValidateRequest, Message, UpdatePassword, UserToken, User
from app.utils import CaptchaService, EmailCodeService, generate_email_code_template, send_email, logger

router = APIRouter(prefix="/users", tags=["users"])


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

@router.get("/me")
def get_user(current_user: CurrentUser):
    return current_user

@router.put("/")
def change_user_info(
        session: SessionDep,
        current_user: CurrentUser,
        user_data: dict = Body(...),
) -> Dict[str, Any]:
    try:
        # Extract username from request body
        username = user_data.get("username")

        if not username:
            return {"code": 400, "message": "用户名不能为空"}

        # Update username in database
        current_user.username = username
        session.add(current_user)
        session.commit()

        return {"code": 200, "message": "资料修改成功"}

    except Exception as e:
        session.rollback()
        return {"code": 500, "message": f"资料修改失败: {str(e)}"}

@router.get("/validateCode")
async def get_captcha():
    # 调用验证码生成服务
    base64_img, result = await CaptchaService.create_captcha_image_service()
    return {
        "img": base64_img,  # 前端展示的图片Base64
        "validateCodeId": str(result)  # 后端保存的正确结果，用于后续验证
    }


@router.post("/validateCode")
async def validate_code(request: ValidateRequest):
    if request.validate_code_id == request.validate_code:
        is_valid = True
    else:
        is_valid = False
    return {
        "code": 0 if is_valid else 400,
        "msg": "验证成功" if is_valid else "验证码错误或已过期"
    }


@router.post("/emailCode")
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

@router.post("/emailCodeVerification")
async def verify_email_code(request: EmailValidateRequest):
    if not EmailCodeService.validate_code(request.email, request.validateCode):
        raise HTTPException(400, "验证码错误或已过期")
    return {"message": "验证成功"}

@router.get("/")
def get_user(current_user: CurrentUser):
    return current_user

AVATAR_UPLOAD_DIR = "static/uploads/avatars"

@router.post("/avatar")
async def change_user_avatar(
        session: SessionDep,
        current_user: CurrentUser,
        avatar: UploadFile = File(...)
) -> Dict[str, Any]:
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif"]
    if avatar.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPEG, PNG and GIF are allowed."
        )

    # 验证文件大小（2MB限制）
    max_size = 2 * 1024 * 1024  # 2MB
    avatar.file.seek(0, 2)  # 移动到文件末尾
    file_size = avatar.file.tell()
    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 2MB limit."
        )
    avatar.file.seek(0)  # 重置文件指针到开头

    try:
        # 确保上传目录存在
        os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)

        # 生成唯一文件名
        file_ext = os.path.splitext(avatar.filename)[1]
        new_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(AVATAR_UPLOAD_DIR, new_filename)

        # 保存文件
        with open(file_path, "wb") as buffer:
            # 分块读取并写入文件
            while chunk := await avatar.read(1024):
                buffer.write(chunk)

        # 创建可访问的URL路径（根据实际部署调整）
        avatar_url = f"http://localhost:8000/static/uploads/avatars/{new_filename}"

        # 更新用户头像信息
        user = session.get(User, current_user.id)
        if user:
            user.avatar = avatar_url
            session.add(user)
            session.commit()
            session.refresh(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "message": "Avatar updated successfully",
            "avatar_url": avatar_url
        }

    except Exception as e:
        # 清理可能的临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload avatar: {str(e)}"
        )