from pydantic import Field
from pydantic import BaseModel, validator

class Product(BaseModel):
    name: str
    description: str
    price: float
    amount: int
    category_id: int


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    amount: int = Field(1, ge=1)
    category_id: int

    @validator("amount")
    def check_amount(cls, value):
        if value < 1:
            raise ValueError("Amount must be greater than 1")
        return value

    @validator("category_id")
    def check_category_id(cls, value):
        if not value:
            raise ValueError("Category ID is required")
        return value