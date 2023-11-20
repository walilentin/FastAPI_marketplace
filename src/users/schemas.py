from typing import Optional
from fastapi_users import schemas
from pydantic import UUID4

class UserRead(schemas.BaseUser):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    balance: float
    role_id: int
    class Config:
        from_attributes = True


class UserUpdate(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    role_id: int

    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False