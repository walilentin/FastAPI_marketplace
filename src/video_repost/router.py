from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Repost
from .schemas import RepostCreate
from ..database import get_async_session
from ..users.base_config import fastapi_users
from ..users.manager import get_user_manager

router = APIRouter(prefix="/reposts", tags=["reposts"])

@router.post("/")
async def create_repost(repost: RepostCreate,
                        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
                        session: AsyncSession = Depends(get_async_session)):
    new_repost = Repost(**repost.dict(), user_id=current_user.id)
    session.add(new_repost)
    await session.commit()
    await session.refresh(new_repost)
    return new_repost

@router.get("{repost_id}")
async def get_repost(repost_id: int, session: AsyncSession = Depends(get_async_session)):
    repost = await session.query(Repost).filter(Repost.id == repost_id).first()
    if repost is None:
        raise HTTPException(status_code=404, detail="Repost not found")
    return repost

@router.delete("{repost_id}", response_model=dict)
async def delete_repost(repost_id: int, session: AsyncSession = Depends(get_async_session)):
    repost = await session.query(Repost).filter(Repost.id == repost_id).first()
    if repost is None:
        raise HTTPException(status_code=404, detail="Repost not found")
    session.delete(repost)
    await session.commit()
    return {"message": "Repost deleted"}
