# app/api/api_v1/item_endpoints.py
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite

from app.schemas.item_schema import ItemCreate, ItemResponse
from app.crud.items_crud import save_item, get_item_by_id, list_items, update_item_by_id, delete_item_by_id
from app.core.database import get_db_items
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/items/", dependencies=[Depends(get_current_user)])
async def create_item(item: ItemCreate, db: aiosqlite.Connection = Depends(get_db_items)):
    item_id = await save_item(db, item.dict(exclude_unset=True))
    created_item = await get_item_by_id(db, item_id)
    return created_item


@router.get("/items/{item_id}", response_model=ItemResponse, dependencies=[Depends(get_current_user)])
async def read_item(item_id: int, db: aiosqlite.Connection = Depends(get_db_items)):
    item_tuple = await get_item_by_id(db, item_id)
    if item_tuple is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = {"id": item_tuple[0], "name": item_tuple[1], "description": item_tuple[2], "price": item_tuple[3],
                 "tax": item_tuple[4]}
    item = ItemResponse(**item_dict)
    return item


@router.get("/items/", dependencies=[Depends(get_current_user)])
async def read_items(db: aiosqlite.Connection = Depends(get_db_items)):
    items = await list_items(db)
    return items


@router.put("/items/{item_id}", dependencies=[Depends(get_current_user)])
async def update_item(item_id: int, item: ItemCreate, db: aiosqlite.Connection = Depends(get_db_items)):
    await update_item_by_id(db, item_id, item.dict(exclude_unset=True))
    updated_item = await get_item_by_id(db, item_id)
    return updated_item


@router.delete("/items/{item_id}", dependencies=[Depends(get_current_user)])
async def delete_item(item_id: int, db: aiosqlite.Connection = Depends(get_db_items)):
    await delete_item_by_id(db, item_id)
    return {"message": "Item successfully deleted"}
