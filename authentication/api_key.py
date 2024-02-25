import secrets
import base64
from fastapi import HTTPException, status, Request


def get_basic_api_key(request: Request):
    """
    Get the basic API key from the request header

    Args:
        request: Request object

    Returns:
        str: API key
    """
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )
    prefix = "Basic"
    if authorization.startswith(prefix):
        base64_api_key = authorization[len(prefix):].strip()
        api_key = base64.b64decode(base64_api_key).decode("utf-8").strip()
        token = read_token()
        if api_key == token:
            return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
    )


def read_token():
    """
    Read the API key from the file

    Returns:
        str: API key
    """
    with open("authentication/basic_api_key.txt", "r") as file:
        return file.read().strip()


def create_and_encode_api_key():
    """
    Create and encode the API key

    Returns:
        str: Encoded API key
    """
    # Generate a random API key
    api_key = secrets.token_urlsafe(32)  # 32 bytes of randomness

    # Encode the API key in base64
    base64_api_key = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")

    return base64_api_key


def write_token():
    """
    Write the API key to the file

    Returns:
        str: API key
    """
    api_key = create_and_encode_api_key()
    with open("basic_api_key.txt", "w") as file:
        file.write(api_key)
    return api_key
