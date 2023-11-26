from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update, delete, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.database import get_async_session
from src.users.base_config import current_user_admin
from src.users.models import User

from src.users.schemas import UserUpdate, UserCreate

router = APIRouter(prefix="/admin", tags=["Admin-Panel"])

templates = Jinja2Templates(directory="/home/valik/Стільниця/FastAPI-like-TikTok/src/templates")

@router.patch("/update-user/{user_id}", dependencies=[Depends(current_user_admin)])
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).filter(User.id == user_id))
    update_data = user_update.dict(exclude_unset=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(update(User).where(User.id == user_id).values(update_data))
    await session.commit()

    return {"message": f"User with ID {user_id} updated successfully"}


@router.post("/create-user", dependencies=[Depends(current_user_admin)])
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(**user_create.dict())
    session.add(new_user)
    await session.commit()
    return {"message": "User created successfully"}


@router.get("/list-users", dependencies=[Depends(current_user_admin)])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    user_table = User.__table__
    users = await session.execute(select(user_table))

    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return {"users": user_list}


@router.delete("/delete-user/{user_id}", dependencies=[Depends(current_user_admin)])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).filter(User.id == user_id))
    if not user.scalar():
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()

    return {"message": f"User with ID {user_id} deleted successfully"}


@router.get("/", dependencies=[Depends(current_user_admin)])
async def home(request: Request):
    return templates.TemplateResponse("admins.html", {"request": request})
