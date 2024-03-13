# auth/security.py

import os
import secrets
import base64
from fastapi import HTTPException, status, Request
from dotenv import load_dotenv

load_dotenv()


def get_api_key(request: Request, scheme: str = "Bearer") -> str:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    if scheme == "Bearer":
        print("hello bearer")
        token = os.getenv("BEARER_API_KEY")
        prefix = "Bearer"
    elif scheme == "Basic":
        print("hello basic")
        token = os.getenv("BASIC_API_KEY")
        prefix = "Basic"
    else:
        print("hello")
        print(f"Unsupported authentication scheme: {scheme}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unsupported authentication scheme"
        )

    if authorization.startswith(prefix):
        api_key = authorization[len(prefix):].strip()
        if scheme == "Basic":
            api_key = base64.b64decode(api_key).decode("utf-8").strip()
        if api_key == token:
            return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
    )


def create_and_store_api_key(scheme: str = "Bearer") -> str:
    api_key = secrets.token_urlsafe(32)  # 32 bytes of randomness
    if scheme == "Basic":
        api_key = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")

    if scheme == "Bearer":
        os.environ["BEARER_API_KEY"] = api_key
    elif scheme == "Basic":
        os.environ["BASIC_API_KEY"] = api_key
    else:
        raise ValueError("Unsupported authentication scheme")

    return api_key
