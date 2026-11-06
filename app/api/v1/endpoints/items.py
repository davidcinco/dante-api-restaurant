from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.items import Item as ItemModel
from app.schemas.items import Item

router = APIRouter()

def find_item(item_id: int) -> Item:
    for item in items:
        if item.item_id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/")
def root():
    return {"Hello": "World"}

@router.get("/items/", response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    return db.scalars(select(ItemModel)).all()

@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/", response_model=Item, status_code=201)
def create_item(data: ItemCreate):
    new_id = max((item.item_id for item in items), default=0) + 1
    item = Item(item_id=new_id, item_name=data.item_name, category_id=data.category_id, price=data.price)
    items.append(item)
    return item

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate):
    item = find_item(item_id)
    item.item_name = updated_item.item_name
    item.price = updated_item.price
    return item

@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    items.remove(find_item(item_id))