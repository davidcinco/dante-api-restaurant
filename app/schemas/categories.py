from pydantic import BaseModel

class CategoryCreate(BaseModel):
    category_name: str

class Category(CategoryCreate):
    category_id: int