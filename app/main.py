from fastapi import FastAPI
from app.api.api_v1.item_endpoints import router as item_router
from app.auth.routers import router as auth_router
from app.core.database import create_start_app_handler

app = FastAPI(title="Item Management API", version="1.0.0", description="API for managing items")

# app.add_event_handler("startup", create_start_app_handler(app))
# @app.on_event("startup")
# async def startup_event():
#     # Initialize database and tables
#     await create_table()


# Include routers
app.include_router(item_router, prefix="/api/v1/items", tags=["items"])
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
