# LostItem model
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user_model import User


class LostItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    image_url: Optional[str] = None
    location_text: Optional[str] = None
    map_lat: Optional[float] = None
    map_lng: Optional[float] = None
    contact_info: Optional[str] = None

class LostItemCreate(LostItemBase):
    pass


class LostItem(LostItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="lost_items")
    status: str = Field(default="unclaimed")  # unclaimed, claimed
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class LostItemPublic(LostItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    status: str
    created_at: datetime

class LostItemsPublic(SQLModel):
    data: list[LostItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str
