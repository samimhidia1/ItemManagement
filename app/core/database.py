# app/core/database.py

import aiosqlite

DATABASE_ITEMS_URL = 'database/items.db'
DATABASE_USERS_URL = 'database/users.db'


async def get_db_items() -> aiosqlite.Connection:
    async with aiosqlite.connect(DATABASE_ITEMS_URL) as db:
        yield db


async def get_db_users() -> aiosqlite.Connection:
    async with aiosqlite.connect(DATABASE_USERS_URL) as db:
        yield db


async def create_table_items():
    async with aiosqlite.connect(DATABASE_ITEMS_URL) as db:
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


async def create_table_users():
    async with aiosqlite.connect(DATABASE_USERS_URL) as db:
        async with db.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL);
            ''')
        await db.commit()


def create_start_app_handler(app):
    async def start_app() -> None:
        await create_table_items()
        await create_table_users()

    return start_app
