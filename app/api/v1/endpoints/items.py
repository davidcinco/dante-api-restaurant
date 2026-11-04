from fas0000000000000000000000000000000000000000tapi import APIRouter, HTTPException
from app.schemas.items import ItemCreate, Item

router = APIRouter()

items: list[Item] = [
    Item(item_id=1, item_name="Item 1", price=10.0),
    Item(item_id=2, item_name="Item 2", price=33.49),
    Item(item_id=3, item_name="Item 3", price=15.29),
    Item(item_id=4, item_name="Item 4", price=10.99),
    Item(item_id=5, item_name="Item 5", price=4.99)
]

def find_item(item_id: int) -> Item:
    for item in items:
        if item.item_id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/")
def root():
    return {"Hello": "World"}

@router.get("/items/", response_model=list[Item])
def get_items():
    return items

@router.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    return find_item(item_id)

@router.post("/items/", response_model=Item, status_code=201)
def create_item(data: ItemCreate):
    new_id = max((item.item_id for item in items), default=0) + 1
    item = Item(item_id=new_id, item_name=data.item_name, price=data.price)
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