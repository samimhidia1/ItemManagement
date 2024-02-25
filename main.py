import sentry_sdk
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from authentication.api_key import get_basic_api_key
from database import save_item, get_db, get_item_by_id, list_items, update_item_by_id, delete_item_by_id
from models import Item

sentry_sdk.init(
    dsn="https://e706f3f7e7f87c42358f0fe9c64e3414@o4504293372985344.ingest.sentry.io/4506807097491456",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


app = FastAPI(
    title="Item Management API for GPTs",
    description="This is a simple API to manage items. It is part of a tutorial for custom actions in GPTs.",
    version="1.0.0",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Item Management API for GPTs"}


@app.get("/items/{item_id}", dependencies=[Depends(get_basic_api_key)])
async def read_item(item_id: int, db=Depends(get_db)):
    db_item = await get_item_by_id(db, item_id)
    if db_item is None:
        print(f"Item with id {item_id} is None")
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/items/", dependencies=[Depends(get_basic_api_key)])
async def create_item(item: Item, db=Depends(get_db)):
    await save_item(db, item)
    return item


# list items
@app.get("/items/", dependencies=[Depends(get_basic_api_key)])
async def list_all_items(db=Depends(get_db)):
    items = await list_items(db)
    return items


@app.put("/items/{item_id}", dependencies=[Depends(get_basic_api_key)])
async def update_item(item_id: int, item: Item, db=Depends(get_db)):
    db_item = await get_item_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await update_item_by_id(db, item_id, item)
    return item


@app.delete("/items/{item_id}", dependencies=[Depends(get_basic_api_key)])
async def delete_item(item_id: int, db=Depends(get_db)):
    db_item = await get_item_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await delete_item_by_id(db, item_id)
    return {"message": "Item deleted successfully"}


@app.get("/privacy-policy")
async def privacy_policy():
    return FileResponse("privacy_policy.html")
