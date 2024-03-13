import aiosqlite
from fastapi import FastAPI

DATABASE_URL = 'database/items.db'


async def get_db() -> aiosqlite.Connection:
    async with aiosqlite.connect(DATABASE_URL) as db:
        yield db


async def create_table():
    async with aiosqlite.connect(DATABASE_URL) as db:
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


def create_start_app_handler(app: FastAPI) -> callable:
    async def start_app() -> None:
        await create_table()

    return start_app
