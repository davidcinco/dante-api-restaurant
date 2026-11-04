from pydantic import BaseModel

class ItemCreate(BaseModel):
    item_name: str
    category_id: int
    price: float

class Item(ItemCreate):
    item_id: int