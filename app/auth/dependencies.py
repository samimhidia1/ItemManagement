# app/dependencies.py
import os
from typing import Generator
import aiosqlite
from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException

load_dotenv()


# Database Connection Dependency
async def get_db() -> Generator:
    async with aiosqlite.connect("database/items.db") as db:  # Adjust path as needed
        yield db


# Assuming a function to verify API keys exists
async def verify_api_key(api_key: str) -> bool:
    # decode the base64 encoded api key
    return api_key == os.getenv("BASIC_API_KEY")


# User Authentication Dependency
async def get_current_user(api_key: str = Header(...)):
    if not await verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return {"api_key": api_key}
