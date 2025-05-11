import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user_model import User


# Comment model
class CommentBase(SQLModel):
    content: str = Field(min_length=1, max_length=255)

class CommentCreate(CommentBase):
    help_post_id: Optional[uuid.UUID] = None

class Comment(CommentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    help_post_id: Optional[uuid.UUID] = Field(default=None, foreign_key="helppost.id")
    created_at: datetime = Field(default_factory=datetime.now)

class CommentPublic(CommentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    help_post_id: Optional[uuid.UUID]
    created_at: datetime

class CommentsPublic(SQLModel):
    data: list[Comment]
    count: int

# Like model
class Like(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    help_post_id: Optional[uuid.UUID] = Field(default=None, foreign_key="helppost.id")


# Report model
class Report(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reporter_id: uuid.UUID = Field(foreign_key="user.id")
    target_type: str  # e.g., 'item', 'help_post', 'comment'
    target_id: uuid.UUID
    reason: str
    created_at: datetime = Field(default_factory=datetime.now)

class ReportsPublic(SQLModel):
    data: list[Report]
    count: int

# Notification model
class Notification(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    content: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

class NotificationsPublic(SQLModel):
    data: list[Notification]
    count: int

# Generic message
class Message(SQLModel):
    message: str