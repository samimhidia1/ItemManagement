import secrets

from fastapi import HTTPException, status, Request

from authentication.api_key import read_token


def get_bearer_api_key(request: Request) -> str:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    prefix = "Bearer"
    if authorization.startswith(prefix):
        api_key = authorization[len(prefix):].strip()
        token = read_token()
        if api_key == token:
            return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
    )


def create_bearer_api_key() -> str:
    """
    Create and encode the API key

    Returns:
        str: Encoded API key
    """
    # Generate a random API key
    api_key = secrets.token_urlsafe(32)  # 32 bytes of randomness

    return api_key


def read_bearer_token() -> str:
    """
    Read the API key from the file

    Returns:
        str: API key
    """
    with open("bearer_api_key.txt", "r") as file:
        return file.read().strip()


def write_bearer_token(token: str) -> None:
    """
    Write the API key to the file

    Args:
        token (str): API key
    """
    with open("bearer_api_key.txt", "w") as file:
        file.write(token)


def create_and_write_bearer_token():
    """
    Create and write the API key to the file

    Returns:
        str: API key
    """
    token = create_bearer_api_key()
    write_bearer_token(token)
    return token


# @app.get("/items/{item_id}", dependencies=[Depends(get_bearer_api_key)])
# @app.post("/items/", dependencies=[Depends(get_bearer_api_key)])
