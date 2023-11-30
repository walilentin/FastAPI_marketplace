from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.basket.models import Basket
from src.database import get_async_session
from src.product.models import Product
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager

router = APIRouter(prefix="/basket")

@router.post("/add-to-basket/{product_id}")
async def create_product(
        product_id: int,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
):

    product = await session.execute(select(Product).filter_by(id=product_id))
    if product.scalar() is None:
        raise HTTPException(status_code=404, detail="Product not found")

    stmt = Basket(user_id=current_user.id, product_id=product_id)
    session.add(stmt)
    await session.commit()

    return {"message": "Product added to basket successfully"}
