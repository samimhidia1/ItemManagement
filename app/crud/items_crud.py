# app/crud/items_crud.py
from typing import List

import aiosqlite


async def save_item(db: aiosqlite.Connection, item_data: dict) -> int:
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO items (name, description, price, tax) VALUES (?, ?, ?, ?)",
            (item_data["name"], item_data["description"], item_data["price"], item_data.get("tax"))
        )
        await db.commit()
        return cursor.lastrowid


async def get_item_by_id(db: aiosqlite.Connection, item_id: int) -> dict:
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = await cursor.fetchone()
        return item


async def list_items(db: aiosqlite.Connection) -> list:
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM items")
        items = await cursor.fetchall()
        return items


async def update_item_by_id(db: aiosqlite.Connection, item_id: int, item_data: dict) -> None:
    async with db.cursor() as cursor:
        await cursor.execute(
            "UPDATE items SET name = ?, description = ?, price = ?, tax = ? WHERE id = ?",
            (item_data["name"], item_data["description"], item_data["price"], item_data.get("tax"), item_id)
        )
        await db.commit()


async def delete_item_by_id(db: aiosqlite.Connection, item_id: int) -> None:
    async with db.cursor() as cursor:
        await cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        await db.commit()
