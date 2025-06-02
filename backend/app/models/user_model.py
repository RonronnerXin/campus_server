import uuid

from sqlmodel import SQLModel, Field, Relationship
from typing import List
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=40)
    username: str | None = Field(default=None, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "user"  # 明确指定表名
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    lost_items: list["LostItem"] = Relationship(back_populates="owner")
    blog_posts: list["BlogPost"] = Relationship(back_populates="author")
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)
    avatar: str | None = Field(default=None, max_length=255)
    dept: str | None = Field(default=None, max_length=255)
    comments: list["Comment"] = Relationship(back_populates="user")



class UserLogin(UserBase):
    password: str


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=6, max_length=40)
    username: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class UserToken(Token):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)  # 用户ID
    username: str  # 用户名
    avatar: str  # 头像路径（可选）

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=6, max_length=40)
    new_password: str = Field(min_length=6, max_length=40)

class ValidateRequest(SQLModel):
    validate_code_id: str = Field(alias="validateCodeId")
    validate_code: str = Field(alias="validateCode")

class EmailValidateRequest(SQLModel):
    validateCode: str = Field("")
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore


class EmailCodeRequest(SQLModel):
    email: EmailStr

class Message(SQLModel):
    message: str