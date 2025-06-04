import uuid
from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from sqlmodel import func, select, Session
from pydantic import parse_obj_as

from app.api.deps import CurrentUser, SessionDep
from app.models.lostItem_model import (
    LostItem, LostItemCreate, LostItemPublic, LostItemsPublic,
    ItemImage, ItemType, ItemCategory, ItemStatus, ContactType,
    Message
)
from app.utils import upload_file_to_storage

router = APIRouter(prefix="/lost-items", tags=["lost_items"])


@router.get("/", response_model=LostItemsPublic)
def read_lost_items(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 20,
        type: ItemType = None,
        category: ItemCategory = None,
        status: ItemStatus = None,
        q: str = None,
) -> Any:
    """
    检索失物招领信息列表。
    支持筛选、分页和搜索。
    """
    # 构建基本查询
    query = select(LostItem)
    count_query = select(func.count()).select_from(LostItem)

    # 应用筛选条件
    if type:
        query = query.where(LostItem.type == type)
        count_query = count_query.where(LostItem.type == type)

    if category:
        query = query.where(LostItem.category == category)
        count_query = count_query.where(LostItem.category == category)

    if status:
        query = query.where(LostItem.status == status)
        count_query = count_query.where(LostItem.status == status)

    # 搜索功能
    if q:
        search_filter = (
                (LostItem.title.contains(q)) |
                (LostItem.description.contains(q)) |
                (LostItem.location.contains(q))
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    # 非管理员只能看到自己的物品或公开的物品
    # if not current_user.is_superuser:
        # 允许用户看到所有公开物品和自己的物品
    query = query.where((LostItem.status != ItemStatus.EXPIRED) | (LostItem.owner_id == current_user.id))
    count_query = count_query.where(
        (LostItem.status != ItemStatus.EXPIRED) | (LostItem.owner_id == current_user.id))

    # 执行查询
    total_count = session.exec(count_query).one()
    items = session.exec(query.order_by(LostItem.created_at.desc()).offset(skip).limit(limit)).all()

    # 计算总页数
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # 获取每个物品的图片
    result_items = []
    for item in items:
        # 获取物品的图片
        images_query = select(ItemImage.image_url).where(ItemImage.item_id == item.id)
        image_urls = session.exec(images_query).all()

        # 转换为公开模型
        item_dict = item.model_dump()
        item_dict["images"] = image_urls
        item_dict["owner_username"] = current_user.username
        item_dict["owner_avatar"] = current_user.avatar
        result_items.append(parse_obj_as(LostItemPublic, item_dict))
        print(result_items)
    return LostItemsPublic(data=result_items, count=total_count, total_pages=total_pages)


@router.get("/my", response_model=LostItemsPublic)
def read_my_lost_items(
        session: SessionDep,
        current_user: CurrentUser,
        skip: int = 0,
        limit: int = 20,
        status: ItemStatus = None,
) -> Any:
    """
    获取当前用户发布的失物招领信息。
    """
    # 构建基本查询
    query = select(LostItem).where(LostItem.owner_id == current_user.id)
    count_query = select(func.count()).select_from(LostItem).where(LostItem.owner_id == current_user.id)

    # 应用状态筛选
    if status:
        query = query.where(LostItem.status == status)
        count_query = count_query.where(LostItem.status == status)

    # 执行查询
    total_count = session.exec(count_query).one()
    items = session.exec(query.order_by(LostItem.created_at.desc()).offset(skip).limit(limit)).all()

    # 计算总页数
    total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

    # 获取每个物品的图片
    result_items = []
    for item in items:
        # 获取物品的图片
        images_query = select(ItemImage.image_url).where(ItemImage.item_id == item.id)
        image_urls = session.exec(images_query).all()

        # 转换为公开模型
        item_dict = item.model_dump()
        item_dict["images"] = image_urls
        item_dict["owner_username"] = current_user.username
        item_dict["owner_avatar"] = current_user.avatar
        result_items.append(parse_obj_as(LostItemPublic, item_dict))

    return LostItemsPublic(data=result_items, count=total_count, total_pages=total_pages)


@router.get("/{id}", response_model=LostItemPublic)
def read_lost_item(
        session: SessionDep,
        id: uuid.UUID,
        current_user: CurrentUser,
) -> Any:
    """
    通过ID获取失物招领信息详情。
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="物品信息未找到")

    # 检查权限 - 已过期的物品只有所有者和管理员可以查看
    if item.status == ItemStatus.EXPIRED and not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看此信息")

    # 增加浏览次数（如果查看者不是物品所有者）
    if item.owner_id != current_user.id:
        item.views_count += 1
        session.add(item)
        session.commit()
        session.refresh(item)

    # 获取物品的图片
    images_query = select(ItemImage.image_url).where(ItemImage.item_id == item.id)
    image_urls = session.exec(images_query).all()

    # 转换为公开模型
    item_dict = item.model_dump()
    item_dict["images"] = image_urls
    item_dict["owner_username"] = current_user.username
    item_dict["owner_avatar"] = current_user.avatar

    return parse_obj_as(LostItemPublic, item_dict)


@router.post("/", response_model=LostItemPublic)
async def create_lost_item(
        session: SessionDep,
        current_user: CurrentUser,
        type: ItemType = Form(...),
        title: str = Form(...),
        category: ItemCategory = Form(...),
        description: str = Form(...),
        location: str = Form(...),
        time: datetime = Form(...),
        contact_type: ContactType = Form(...),
        contact_value: str = Form(None),
        hide_contact: bool = Form(False),
        images: List[UploadFile] = File(None),
) -> Any:
    """
    创建新的失物招领信息。
    支持多图片上传。
    """
    # 验证联系方式
    if not hide_contact and not contact_value:
        raise HTTPException(status_code=400, detail="请提供联系方式或选择仅通过站内消息联系")

    # 创建物品记录
    item_data = {
        "type": type,
        "title": title,
        "category": category,
        "description": description,
        "location": location,
        "time": time,
        "contact_type": contact_type,
        "contact_value": contact_value,
        "hide_contact": hide_contact,
        "owner_id": current_user.id,
        "status": ItemStatus.UNCLAIMED
    }

    item = LostItem(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)

    # 处理图片上传
    image_urls = []
    if images:
        for image in images:
            if image.content_type.startswith('image/'):
                contents = await image.read()
                if len(contents) > 3 * 1024 * 1024:  # 限制为3MB
                    continue
                await image.seek(0)
                image_url = await upload_file_to_storage(
                    file=image,
                    folder=f"lost-items/{item.id}",
                    filename=f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
                )
                item_image = ItemImage(item_id=item.id, image_url=image_url, created_at=time)
                session.add(item_image)
                image_urls.append(image_url)

    session.commit()

    # 构造符合 LostItemPublic 的返回数据
    response_data = {
        "id": item.id,
        "type": item.type,
        "title": item.title,
        "category": item.category,
        "description": item.description,
        "location": item.location,
        "time": item.time,
        "contact_type": item.contact_type,
        "contact_value": item.contact_value,
        "hide_contact": item.hide_contact,
        "status": item.status,
        "owner_id": item.owner_id,
        "images": image_urls,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "views_count": item.views_count,
        "owner_username": current_user.username,
        "owner_avatar": current_user.avatar,
    }

    return response_data


@router.put("/{id}", response_model=LostItemPublic)
async def update_lost_item(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        type: ItemType = Form(...),
        title: str = Form(...),
        category: ItemCategory = Form(...),
        description: str = Form(...),
        location: str = Form(...),
        time: datetime = Form(...),
        contact_type: ContactType = Form(...),
        contact_value: str = Form(None),
        hide_contact: bool = Form(False),
        status: ItemStatus = Form(...),
        images: List[UploadFile] = File(None),
        delete_images: List[str] = Query(None),
) -> Any:
    """
    更新失物招领信息。
    支持添加新图片和删除现有图片。
    """
    # 获取物品
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="物品信息未找到")

    # 检查权限
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此信息")

    # 验证联系方式
    if not hide_contact and not contact_value:
        raise HTTPException(status_code=400, detail="请提供联系方式或选择仅通过站内消息联系")

    # 更新物品信息
    item.type = type
    item.title = title
    item.category = category
    item.description = description
    item.location = location
    item.time = time
    item.contact_type = contact_type
    item.contact_value = contact_value
    item.hide_contact = hide_contact
    item.status = status
    item.updated_at = datetime.now()

    session.add(item)

    # 处理图片删除
    if delete_images:
        for image_url in delete_images:
            image = session.exec(
                select(ItemImage).where(
                    (ItemImage.item_id == id) & (ItemImage.image_url == image_url)
                )
            ).first()
            if image:
                session.delete(image)

    # 处理新图片上传
    image_urls = []
    existing_images_query = select(ItemImage.image_url).where(ItemImage.item_id == id)
    existing_images = session.exec(existing_images_query).all()

    if images:
        # 检查图片数量限制
        total_images = len(existing_images) - (len(delete_images) if delete_images else 0) + len(images)
        if total_images > 3:
            raise HTTPException(status_code=400, detail="最多只能上传3张图片")

        for image in images:
            if image.content_type.startswith('image/'):
                # 检查文件大小
                contents = await image.read()
                if len(contents) > 2 * 1024 * 1024:  # 2MB
                    continue

                # 重置文件指针
                await image.seek(0)

                # 上传图片到存储服务
                image_url = await upload_file_to_storage(
                    file=image,
                    folder=f"lost-items/{item.id}",
                    filename=f"{uuid.uuid4()}.{image.filename.split('.')[-1]}"
                )

                # 创建图片记录
                item_image = ItemImage(item_id=item.id, image_url=image_url)
                session.add(item_image)
                image_urls.append(image_url)

    session.commit()
    session.refresh(item)

    # 获取所有图片
    all_images_query = select(ItemImage.image_url).where(ItemImage.item_id == id)
    all_image_urls = session.exec(all_images_query).all()

    # 返回更新后的物品信息
    item_dict = item.model_dump()
    item_dict["images"] = all_image_urls

    return parse_obj_as(LostItemPublic, item_dict)


@router.patch("/{id}/status", response_model=LostItemPublic)
def update_item_status(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
        status: ItemStatus,
) -> Any:
    """
    更新物品状态（认领/未认领/过期）。
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="物品信息未找到")

    # 检查权限
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此信息")

    # 更新状态
    item.status = status
    item.updated_at = datetime.now()

    session.add(item)
    session.commit()
    session.refresh(item)

    # 获取物品的图片
    images_query = select(ItemImage.image_url).where(ItemImage.item_id == item.id)
    image_urls = session.exec(images_query).all()

    # 返回更新后的物品信息
    item_dict = item.model_dump()
    item_dict["images"] = image_urls

    return parse_obj_as(LostItemPublic, item_dict)


@router.delete("/{id}")
def delete_lost_item(
        session: SessionDep,
        current_user: CurrentUser,
        id: uuid.UUID,
) -> Message:
    """
    删除失物招领信息。
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="物品信息未找到")

    # 检查权限
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此信息")

    # 删除相关图片记录
    # 先查询出所有相关图片
    item_images = session.query(ItemImage).filter(ItemImage.item_id == id).all()

    # 逐个删除图片记录
    for image in item_images:
        session.delete(image)

    # 删除物品记录
    session.delete(item)
    session.commit()

    return Message(message="物品信息已成功删除")