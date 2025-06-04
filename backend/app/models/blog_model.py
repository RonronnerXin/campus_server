import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


class BlogCategory(str, Enum):
    TECH = "tech"  # 技术
    LIFE = "life"  # 生活
    STUDY = "study"  # 学习
    TRAVEL = "travel"  # 旅行
    OTHER = "other"  # 其他


class BlogStatus(str, Enum):
    DRAFT = "draft"  # 草稿
    PUBLISHED = "published"  # 已发布


class BlogPostBase(SQLModel):
    __tablename__ = "blogpost"  # 明确指定表名
    title: str = Field(min_length=1, max_length=255)
    category: BlogCategory  # 博客分类
    summary: str = Field(max_length=500)  # 博客摘要
    content: str  # 博客正文内容
    allow_comments: bool = Field(default=True)  # 是否允许评论
    featured: bool = Field(default=False)  # 是否推荐


class BlogPostCreate(BlogPostBase):
    tags: List[str] = []  # 标签列表


class BlogPost(BlogPostBase, table=True):
    __tablename__ = "blogpost"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_id: uuid.UUID = Field(foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="blog_posts")
    status: BlogStatus = Field(default=BlogStatus.DRAFT)
    images: list["BlogImage"] = Relationship(back_populates="blog")
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = Field(default=None)
    views_count: int = Field(default=0)  # 浏览次数
    likes_count: int = Field(default=0)  # 点赞数
    comments_count: int = Field(default=0)  # 评论数
    comments: List["Comment"] = Relationship(back_populates="post")


class Comment(SQLModel, table=True):
    __tablename__ = "comment"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="blogpost.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="comment.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    likes_count: int = Field(default=0)
    post: "BlogPost" = Relationship(back_populates="comments")
    user: Optional["User"] = Relationship(back_populates="comments")
    replies: list["Comment"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Comment.id"}
    )


class CommentLike(SQLModel, table=True):
    __tablename__ = "commentlike"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    comment_id: uuid.UUID = Field(foreign_key="comment.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)


class PostLike(SQLModel, table=True):
    __tablename__ = "postlike"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    post_id: uuid.UUID = Field(foreign_key="blogpost.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

class BlogImage(SQLModel, table=True):
    __tablename__ = "blogimage"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    blog_id: uuid.UUID = Field(foreign_key="blogpost.id")  # 外键声明
    image_url: str
    created_at: datetime = Field(default=datetime.now)
    blog: "BlogPost" = Relationship(back_populates="images")

# 响应模型
class BlogPostPublic(BlogPostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    author_name: str
    author_avatar: str
    status: BlogStatus
    images: List[str] = []  # 简化为图片URL列表
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    views_count: int
    likes_count: int
    comments_count: int
    liked: bool = False  # 当前用户是否点赞
    comments: List[str] = []


class BlogPostsPublic(SQLModel):
    data: List[BlogPostPublic]
    count: int
    total_pages: int


class CommentPublic(SQLModel):
    id: uuid.UUID
    post_id: uuid.UUID
    user_id: uuid.UUID
    user_name: str
    user_avatar: Optional[str]
    parent_id: Optional[uuid.UUID]
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int
    liked: bool = False
    replies: List["CommentPublic"] = []


class CommentsPublic(SQLModel):
    data: List[CommentPublic]
    count: int
    total_pages: int


# 用于消息通知的模型
class Message(SQLModel):
    message: str