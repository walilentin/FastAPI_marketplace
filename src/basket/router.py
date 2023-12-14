from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.basket.models import Basket
from src.database import get_async_session
from src.product.models import Product
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager

router = APIRouter(prefix="/basket")


async def get_basket(session: AsyncSession = Depends(get_async_session),
                     user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
        if user is None:
            return []
        stmt = select(Basket, Product).join(Product).filter(Basket.user_id == user.id)
        result = await session.execute(stmt)
        basket_data = result.scalars().all()

        basket = [
            {"product_id": item.Basket.product_id, "product_name": item.Product.name, "quantity": item.Basket.quantity}
            for item in basket_data]

        return basket


@router.post("/add-to-basket/{product_id}")
async def create_product(
        product_id: int,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
        basket: list = Depends(get_basket)
):
    product = await session.execute(select(Product).filter_by(id=product_id))
    if product.scalar() is None:
        raise HTTPException(status_code=404, detail="Product not found")

    stmt = Basket(user_id=current_user.id, product_id=product_id)
    session.add(stmt)
    await session.commit()

    return {"message": "Product added to basket successfully", "basket": basket}
