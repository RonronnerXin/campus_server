import logging
import secrets
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

import time
import base64
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont

import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError

from app.core import security
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text(encoding="utf-8")
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    try:
        smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
        print(smtp_options)
        if settings.SMTP_TLS:
            smtp_options["tls"] = True
        elif settings.SMTP_SSL:
            smtp_options["ssl"] = True
        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER
        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD
        response = message.send(to=email_to, smtp=smtp_options)
        logger.info(f"send email result: {response}")
    except Exception as e:
        print({"detail": f"邮件发送失败: {str(e)}", "traceback": traceback.format_exc()})

#邮箱发送验证码
def generate_email_code_template(email_to: str, code: str) -> EmailData:
    project_name = "WitNova"
    subject = f"{project_name} - 邮箱验证码"
    html_content = render_email_template(
        template_name="email_code.html",
        context={
            "project_name": project_name,
            "code": code,
            "email": email_to,
            "valid_minutes": int(EmailCodeService.CODE_TTL/60)
        }
    )
    return EmailData(html_content=html_content, subject=subject)

class CaptchaService:
#验证码生成
    @classmethod
    async def create_captcha_image_service(cls):
        # 创建空白图像
        image = Image.new('RGB', (160, 60), color='#EAEAEA')

        # 创建绘图对象
        draw = ImageDraw.Draw(image)

        # 设置字体
        font = ImageFont.truetype(os.path.join(os.path.abspath(os.getcwd()), 'assets', 'font', 'Arial.ttf'), size=30)

        # 生成两个0-9之间的随机整数
        num1 = random.randint(0, 9)
        num2 = random.randint(0, 9)
        # 从运算符列表中随机选择一个
        operational_character_list = ['+', '-', '*']
        operational_character = random.choice(operational_character_list)
        # 根据选择的运算符进行计算
        if operational_character == '+':
            result = num1 + num2
        elif operational_character == '-':
            result = num1 - num2
        else:
            result = num1 * num2
        # 绘制文本
        text = f'{num1} {operational_character} {num2} = ?'
        draw.text((25, 15), text, fill='blue', font=font)

        # 将图像数据保存到内存中
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')

        # 将图像数据转换为base64字符串
        base64_string = base64.b64encode(buffer.getvalue()).decode()

        return [base64_string, result]


class EmailCodeService:
    _storage: Dict[str, Tuple[str, float]] = {}
    CODE_TTL = 300  # 验证码有效期5分钟

    @classmethod
    def generate_code(cls, length: int = 6) -> str:
        """生成数字验证码"""
        return "".join(secrets.choice("0123456789") for _ in range(length))

    @classmethod
    def store_code(cls, email: str, code: str) -> None:
        """存储验证码到内存"""
        cls._storage[email] = (code, time.time() + cls.CODE_TTL)

    @classmethod
    def validate_code(cls, email: str, code: str) -> bool:
        """验证码校验"""
        if email not in cls._storage:
            return False

        stored_code, expire_time = cls._storage[email]
        if time.time() > expire_time:
            del cls._storage[email]
            return False

        return secrets.compare_digest(code, stored_code)

    @classmethod
    def cleanup_expired(cls) -> None:
        """清理过期验证码"""
        now = time.time()
        expired_emails = [
            email for email, (_, expire) in cls._storage.items()
            if now > expire
        ]
        for email in expired_emails:
            del cls._storage[email]


from fastapi import UploadFile
from app.core.config import settings


async def upload_file_to_storage(file: UploadFile, folder: str, filename: str = None) -> str:
    """
    上传文件到存储服务（本地存储或云存储）

    Args:
        file: 要上传的文件
        folder: 存储文件夹路径
        filename: 文件名（如果不提供，将使用原始文件名）

    Returns:
        str: 文件的访问URL
    """
    if not filename:
        filename = file.filename

    # 确保目录存在
    upload_dir = os.path.join(settings.STATIC_DIR, folder)
    os.makedirs(upload_dir, exist_ok=True)

    # 构建文件路径
    file_path = os.path.join(upload_dir, filename)

    # 保存文件
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # 返回文件URL
    return f"{settings.API_URL}/static/{folder}/{filename}"