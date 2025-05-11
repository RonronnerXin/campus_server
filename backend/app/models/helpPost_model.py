import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user_model import User


class HelpPostBase(SQLModel):
    title: str
    content: str
    image_url: Optional[str] = None

class HelpPostCreate(HelpPostBase):
    pass

class HelpPost(HelpPostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="help_posts")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HelpPostPublic(HelpPostBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

class HelpPostsPublic(SQLModel):
    data: list[HelpPostPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str