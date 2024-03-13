# auth/routers.py

from fastapi import APIRouter, Depends
from .dependencies import get_current_user

router = APIRouter()


@router.get("/test-auth")
async def test_auth(user: dict = Depends(get_current_user)):
    return {"user": user}
