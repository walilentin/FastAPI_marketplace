from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.database import get_async_session
from src.product.models import Category
from src.users.base_config import current_user_has_permission, fastapi_users
from src.users.models import User, Role

from src.users.schemas import UserUpdate, UserCreate

router = APIRouter(prefix="/admin", tags=["Admin-Panel"])

templates = Jinja2Templates(directory="/home/valik/Стільниця/FastAPI-like-TikTok/src/templates")


@router.patch("/update-user/{user_id}", dependencies=[Depends(current_user_has_permission("manage_users"))])
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).filter(User.id == user_id))
    update_data = user_update.dict(exclude_unset=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(update(User).where(User.id == user_id).values(update_data))
    await session.commit()

    return {"message": f"User with ID {user_id} updated successfully"}


@router.post("/create-user", dependencies=[Depends(current_user_has_permission("manage_users"))])
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(**user_create.dict())
    session.add(new_user)
    await session.commit()
    return {"message": "User created successfully"}


@router.get("/list-users", dependencies=[Depends(current_user_has_permission("manage_users"))])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    user_table = User.__table__
    users = await session.execute(select(user_table))

    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return {"users": user_list}


@router.delete("/delete-user/{user_id}", dependencies=[Depends(current_user_has_permission("manage_users"))])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).filter(User.id == user_id))
    if not user.scalar():
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()

    return {"message": f"User with ID {user_id} deleted successfully"}

@router.post("/add-category", dependencies=[Depends(current_user_has_permission("manage_products"))])
async def add_category(
        name_category: str,
        session: AsyncSession = Depends(get_async_session),
):
    stmt = Category(name_category=name_category)
    session.add(stmt)
    await session.commit()
    return stmt


@router.delete("/delete-category/{category_id}", dependencies=[Depends(current_user_has_permission("manage_products"))])
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    category = await session.execute(delete(Category).where(Category.id == category_id))
    category = category.scalar()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.commit()
    return {"category": "was deleted"}

@router.post("/change-role", dependencies=[Depends(current_user_has_permission("change_role"))])
async def change_user_role(
    new_role: str,
    current_user: User = Depends(fastapi_users.current_user(active=True, optional=True)),
    session: AsyncSession = Depends(get_async_session),
):
    valid_roles = ["GUEST", "SELLER", "BUYER"]
    if new_role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    role = await session.execute(select(Role).where(Role.name == new_role))
    role = role.scalar()

    if role:
        await session.execute(update(User).where(User.id == current_user.id).values(role_id=role.id))
        await session.commit()
        return {"message": f"Role changed to {new_role}"}
    else:
        raise HTTPException(status_code=404, detail="Role not found")