from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.database import get_async_session
from src.db_curl import BaseService
from src.product.models import Product


class ProductService(BaseService[Product]):
    def __init__(self, db_session: Session):
        super(ProductService, self).__init__(Product, db_session)

    async def create(self, data):
        async with self.db_session as session:
            new_product = self.table(
                name=data.name,
                description=data.description,
                price=data.price,
                seller_id=data.seller_id,
                amount=data.amount,
                category_id=data.category_id,
            )
            session.add(new_product)
            await session.commit()
        return new_product

    async def update(self, data):
        return await super().update(data)


def get_product_service(db_session: AsyncSession = Depends(get_async_session)) -> ProductService:
    return ProductService(db_session)
