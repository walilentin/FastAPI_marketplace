from pydantic import Field
from pydantic import BaseModel
from fastapi import UploadFile

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    amount: int = Field(..., ge=1)
    category_id: int