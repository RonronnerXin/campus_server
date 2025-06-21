import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class ItemType(str, Enum):
    LOST = "lost"  # 寻物启事
    FOUND = "found"  # 招领启事


class ItemCategory(str, Enum):
    CARD = "card"  # 校园卡
    ELECTRONICS = "electronics"  # 电子设备
    BOOKS = "books"  # 书籍资料
    CLOTHING = "clothing"  # 衣物
    OTHER = "other"  # 其他


class ItemStatus(str, Enum):
    UNCLAIMED = "unclaimed"  # 未认领/未找到
    CLAIMED = "claimed"  # 已认领/已找到
    EXPIRED = "expired"  # 已过期


class ContactType(str, Enum):
    PHONE = "phone"  # 手机号
    WECHAT = "wechat"  # 微信
    QQ = "qq"  # QQ

class LostItemBase(SQLModel):
    type: ItemType  # 信息类型：寻物启事/招领启事
    title: str = Field(min_length=1, max_length=255)
    category: ItemCategory  # 物品分类
    description: str = Field(max_length=2000)  # 详细描述
    location: str = Field(max_length=255)  # 丢失/拾获地点
    time: datetime  # 丢失/拾获时间
    contact_type: ContactType  # 联系方式类型
    contact_value: Optional[str] = Field(default=None, max_length=255)  # 联系方式值
    hide_contact: bool = Field(default=False)  # 是否隐藏联系方式
    lat: Optional[float] = Field(default=None, description="纬度")
    lng: Optional[float] = Field(default=None, description="经度")


class LostItemCreate(LostItemBase):
    pass


class LostItem(LostItemBase, table=True):
    __tablename__ = "lostitem"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="lost_items")
    status: ItemStatus = Field(default=ItemStatus.UNCLAIMED)
    images: list["ItemImage"] = Relationship(back_populates="item")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    views_count: int = Field(default=0)  # 浏览次数




# 用于消息通知的模型
class Message(SQLModel):
    message: str


class ItemImage(SQLModel, table=True):
    __tablename__ = "itemimage"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    item_id: uuid.UUID = Field(foreign_key="lostitem.id")  # 外键声明
    image_url: str
    created_at: datetime = Field(default=datetime.now)
    item: "LostItem" = Relationship(back_populates="images")

class LostItemPublic(LostItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    owner_username: str
    owner_avatar: str
    status: ItemStatus
    created_at: datetime
    updated_at: datetime
    views_count: int
    images: List[str] = []  # 简化为图片URL列表

class LostItemsPublic(SQLModel):
    data: List[LostItemPublic]
    count: int
    total_pages: int


class StatusUpdateRequest(SQLModel):
    status: ItemStatus