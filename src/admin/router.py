from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.base_config import current_user_admin
from src.users.manager import User
from src.users.schemas import UserUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.patch("/grand-admins", dependencies=[Depends(current_user_admin)])
async def grand_admins(user_id: int,
                       session: AsyncSession = Depends(get_async_session),
                       ):
    user = await session.execute(select(User).filter(User.id == user_id))
    user = user.scalar()

    await session.execute(update(User).where(User.id == user_id).values(role_id=3))
    await session.commit()
    return {"message": f"Admin access granted to user with ID {user_id}"}


@router.patch("/update-user/{user_id}", dependencies=[Depends(current_user_admin)])
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).filter(User.id == user_id))
    update_data = user_update.dict(exclude_unset=True)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.execute(update(User).where(User.id == user_id).values(update_data))
    await session.commit()

    return {"message": f"User with ID {user_id} updated successfully"}


@router.get("/dashboard", dependencies=[Depends(current_user_admin)])
async def admin_dashboard(
        current_admin_user: User = Depends(current_user_admin)
):
    return {"message": f"Welcome, {current_admin_user.username}, to the admin dashboard!"}
