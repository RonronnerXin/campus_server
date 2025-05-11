import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.lostItem_model import (
    LostItem, LostItemCreate, LostItemPublic, LostItemsPublic,
    Message
)

router = APIRouter(prefix="/lost-items", tags=["lost_items"])


@router.get("/", response_model=LostItemsPublic)
def read_lost_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve lost items.
    """
    if current_user.is_superuser:
        count = session.exec(select(func.count()).select_from(LostItem)).one()
        items = session.exec(select(LostItem).offset(skip).limit(limit)).all()
    else:
        count = session.exec(
            select(func.count())
            .select_from(LostItem)
            .where(LostItem.owner_id == current_user.id)
        ).one()
        items = session.exec(
            select(LostItem)
            .where(LostItem.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        ).all()
    return LostItemsPublic(data=items, count=count)


@router.get("/{id}", response_model=LostItemPublic)
def read_lost_item(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Any:
    """
    Get lost item by ID.
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/", response_model=LostItemPublic)
def create_lost_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: LostItemCreate
) -> Any:
    """
    Create new lost item.
    """
    item = LostItem.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{id}", response_model=LostItemPublic)
def update_lost_item(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    item_in: LostItemCreate,
) -> Any:
    """
    Update a lost item.
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{id}")
def delete_lost_item(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a lost item.
    """
    item = session.get(LostItem, id)
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item)
    session.commit()
    return Message(message="Lost item deleted successfully")
