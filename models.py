from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(..., title="The name of the item", description="The name of the item")
    description: Optional[str] = Field(..., title="item description", description="The description of the item")
    price: float = Field(..., title="The price of the item", description="The price of the item")
    tax: Optional[float] = Field(None, title="The tax of the item", description="The tax of the item")
