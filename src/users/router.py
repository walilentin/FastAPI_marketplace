from http.client import HTTPException
from sqlalchemy import select, update
from src.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.users.base_config import current_superuser
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/user",tags=["User"])

@router.patch('/grand-admins/{user_id}', dependencies=[Depends(current_superuser)])
async def grand_admin(user_id: int,session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role_id == 2:
        raise HTTPException(status_code=404, detail="User has been admin")

    await session.execute(update(User).where(User.id == user_id).values(role_id=2))
    await session.commit()
    return {"message": f"Admin access granted to user with ID {user_id}"}

@router.patch('/remove-admins/{user_id}', dependencies=[Depends(current_superuser)])
async def grand_admin(user_id: int,session: AsyncSession = Depends(get_async_session)):

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(update(User).where(User.id == user_id).values(role_id=1))
    await session.commit()
    return {"message": f"Admin access remove to user with ID {user_id}"}
