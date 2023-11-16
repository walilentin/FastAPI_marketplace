from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.comment.models import Comment
from src.comment.schemas import CommentCreate
from src.database import get_async_session
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager

comment = APIRouter(prefix="/comments", tags=["Comments"])

@comment.post("")
async def create_comment(comment: CommentCreate, video_id: int,
                         session: AsyncSession = Depends(get_async_session),
                         current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
    stmt = insert(Comment).values(**comment.dict(),video_id=video_id,user_id=current_user.id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@comment.delete("/{comment_id}/delete")
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_async_session)):
    # Спочатку перевіряємо, чи існує коментар з вказаним ідентифікатором
    comment = await session.execute(select(Comment).filter(Comment.id == comment_id))

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Видаляємо коментар з бази даних
    await session.execute(delete(Comment).where(Comment.id == comment_id))
    await session.commit()

    return {"status": "success"}