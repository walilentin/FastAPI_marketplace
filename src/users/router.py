from fastapi import APIRouter, Depends, HTTPException
from http.client import HTTPException
from sqlalchemy import select, delete, update
from src.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.product.schemas import ProductCreate
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/user",tags=["User"])


@router.patch('/grand_admin/{user_id}')
async def grand_admin(user_id: int,
                      current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
                      session: AsyncSession = Depends(get_async_session),
                      ):
    if current_user.role_id == 2:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.role_id == 2:
            raise HTTPException(status_code=404, detail="User has been admin")
        await session.execute(
            update(User).where(User.id == user_id).values(role_id=2)
        )
        await session.commit()
        return {"message": f"Admin access granted to user with ID {user_id}"}
    else:
        return {"message": "You are not admin"}

@router.patch('/remove_admin/{user_id}')
async def grand_admin(user_id: int,
                      current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
                      session: AsyncSession = Depends(get_async_session),
                      ):
    if current_user.role_id == 3:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.execute(
            update(User).where(User.id == user_id).values(role_id=1)
        )
        await session.commit()
        return {"message": f"Admin access remove to user with ID {user_id}"}
    else:
        return {"message": "You are not admin"}