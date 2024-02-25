import aiosqlite
from typing import Optional, Tuple
import asyncio
from models import Item


async def get_db() -> aiosqlite.Connection:
    conn = await aiosqlite.connect('items.db')
    return conn


async def get_item_by_id(db: aiosqlite.Connection, item_id: int) -> Optional[Tuple]:
    """
    Get item by id from the database
    Args:
        db:
        item_id:

    Returns:
        Optional[Tuple]: item
    """
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
        item = await cursor.fetchone()
    return item


async def list_items(db: aiosqlite.Connection) -> list[Tuple]:
    """
    List all items from the database
    Args:
        db:

    Returns:
        list[Tuple]: items list with tuples and their ids
    """
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM items")
        items = await cursor.fetchall()
    return items


async def delete_item_by_id(db: aiosqlite.Connection, item_id: int) -> None:
    async with db.cursor() as cursor:
        await cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    await db.commit()


async def update_item_by_id(db: aiosqlite.Connection, item_id: int, item: Item) -> None:
    async with db.cursor() as cursor:
        await cursor.execute("UPDATE items SET name=?, description=?, price=?, tax=? WHERE id=?",
                             (item.name, item.description, item.price, item.tax, item_id))
    await db.commit()


async def save_item(db: aiosqlite.Connection, item: Item) -> None:
    async with db.cursor() as cursor:
        await cursor.execute("INSERT INTO items (name, description, price, tax) VALUES (?, ?, ?, ?)",
                             (item.name, item.description, item.price, item.tax))
    await db.commit()


async def create_table(db: aiosqlite.Connection) -> None:
    async with db.cursor() as cursor:
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS items
            (id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            tax REAL);
        ''')
    await db.commit()


async def main():
    db = await get_db()
    await create_table(db)
    item_1 = Item(name="ChatGPT", description="OpenAI GPT-3", price=20.0)
    await save_item(db, item_1)
    item_2 = Item(name="LLAMA", description="Opensource LLM", price=0.1, tax=5.0)
    await save_item(db, item_2)
    item_3 = Item(name="GPT-3", description="OpenAI GPT-3", price=20.0)
    await save_item(db, item_3)
    print(await get_item_by_id(db, 1))
    print(await get_item_by_id(db, 2))
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
