from typing import Generic, Type, Optional, TypeVar

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.table = model
        self.db_session = db_session

    async def get_one(self, id):
        async with self.db_session as session:
            db_item = await session.execute(
                select(self.table).filter(self.table.id == id)
            )
            db_item = db_item.scalar()
        if not db_item:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_item

    async def get_list(self, limit: Optional[int] = None):
        async with self.db_session as session:
            query = await session.execute(
                select(self.table).limit(limit).order_by(-self.table.id.desc())
            )
            return query.scalars().all()

    async def create(self, data):
        async with self.db_session as session:
            item = self.table(**data.dict())
            session.add(item)
            await session.commit()
        return item

    async def update(self, data):
        async with self.db_session as session:
            await session.execute(
                update(self.table),
                [data.dict()],
            )
            await session.commit()
        return await self.get_one(data.id)

    async def delete(self, id):
        async with self.db_session as session:
            await session.execute(delete(self.table).filter(self.table.id == id))
            await session.commit()
        return None

    async def get(self, **kwargs):
        async with self.db_session as session:
            result = await session.execute(select(self.table).filter_by(**kwargs))
            return result.scalar()