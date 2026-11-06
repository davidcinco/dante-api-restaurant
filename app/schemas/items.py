from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class ItemCreate(BaseModel):
    item_name: str
    category_id: int
    price: float

class Item(ItemCreate):
    model_config = ConfigDict(from_attributes=True)
    item_id: int