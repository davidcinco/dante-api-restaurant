from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.items import Item as ItemModel
from app.schemas.items import Item, ItemCreate

router = APIRouter()

#get endpoints
@router.get("/", response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    return db.scalars(select(ItemModel)).all()

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

#post endpoints
@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    item = ItemModel(item_name=data.item_name, category_id=data.category_id, price=data.price)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

#put endpoints
@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in updated_item.model_dump().items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item

#delete endpoints
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()