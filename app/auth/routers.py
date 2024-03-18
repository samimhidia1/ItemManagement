# app/auth/routers.py

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from .dependencies import get_current_user, create_access_token, get_password_hash, verify_password, decode_access_token
from datetime import timedelta
from app.models.user import User, UserCreate
from app.core.database import get_db_items, get_db_users
import aiosqlite

router = APIRouter()


async def check_username_taken(username: str, db: aiosqlite.Connection):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = await cursor.fetchone()
    return user is not None


async def create_user(db: aiosqlite.Connection, username: str, hashed_password: str):
    cursor = await db.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                              (username, hashed_password))
    await cursor.close()
    await db.commit()


@router.post("/register")
async def register(user: UserCreate, db: aiosqlite.Connection = Depends(get_db_users)):
    # Check if the username is already taken
    if await check_username_taken(user.username, db):
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Store the user's information in your database, including the hashed password
    await create_user(db, user.username, hashed_password)

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(response: Response, user: User, db: aiosqlite.Connection = Depends(get_db_users)):
    # Validate the user's credentials here
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        user_data = await cursor.fetchone()

    if user_data is None or not verify_password(user.hashed_password, user_data[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # If the credentials are valid, generate a new token for the user
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=15))

    # Set the access token as a cookie
    response.set_cookie(key="access_token", value=access_token)

    return {"message": "Logged in successfully"}


@router.get("/users/me")
async def read_users_me(request: Request, db: aiosqlite.Connection = Depends(get_db_users)):
    # Get the access token from the cookies
    access_token = request.cookies.get("access_token")

    # If the access token is None, the user is not logged in
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Decode the access token
    payload = decode_access_token(access_token)

    # Get the username from the payload
    username = payload.get("sub")

    # Retrieve the all the user's information from the database email, full_name, disabled
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = await cursor.fetchone()

    # If the user is None, the access token is invalid
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")

    print(user)
    # Return the user's information
    return {"username": user[1], "email": user[2], "full_name": user[3], "disabled": user[4]}


# existing routes...
@router.get("/test-auth")
async def test_auth(user: dict = Depends(get_current_user)):
    return {"user": user}
