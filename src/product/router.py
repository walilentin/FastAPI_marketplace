from http.client import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.product.models import Product, Order, Review, Category
from src.product.schemas import ProductCreate
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("/add_product")
async def create_product(
        product: ProductCreate,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
):
    if current_user:
        stmt = Product(seller_id=current_user.id, **product.dict())
        session.add(stmt)
        await session.commit()
        return stmt
    else:
        return {"message": "you not auth"}

@router.post("/add_category")
async def add_category(
        name_category: str,
        session: AsyncSession = Depends(get_async_session),
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
):
    if current_user.role_id == 2:
        stmt = Category(name_category=name_category)

        session.add(stmt)
        await session.commit()
        return stmt
    else:
        return {"message":"you not admin"}

@router.delete("/delete_category/{category_id}")
async def delete_category(
        category_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
):
    if current_user:
        if current_user.role_id == 2:
            await session.execute(delete(Category).where(Category.id == category_id))
            await session.commit()
            return {"category": "was deleted"}
        else:
            return {"message": "you not admin"}
    else:
        return {"message": "you not auth"}

@router.delete("/delete_product/{product_id}")
async def delete_product(
        product_id: int,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
):
    if current_user:
        product = await session.execute(select(Product).filter(Product.id == product_id))
        product = product.scalar()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        if current_user.id != product.seller_id:
            raise HTTPException(status_code=403, detail="Permission denied")

        # Видаляємо коментар з бази даних
        await session.execute(delete(Product).where(Product.id == product_id))
        await session.commit()

        return {"status": "success"}
    else:
        return {"message": "you not auth"}

@router.post("/buy_product/{product_id}")
async def buy_product(
        product_id: int,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session)):
    if current_user:
        product = await session.execute(select(Product).filter(Product.id == product_id))
        product = product.scalar()
        if current_user.id == product.seller_id:
            raise HTTPException(status_code=404, detail="Seller cannot buy his product")
        elif not product:
            raise HTTPException(status_code=404, detail="Products not found")
        elif product.amount < 1:
            raise HTTPException(status_code=400, detail="Product is out of stock")
        else:
            if current_user.balance >= product.price:  # перевірка чи є у користувача достатня кількість валюти
                order = Order(buyer_id=current_user.id, seller_id=product.seller_id, item_id=product.id)
                session.add(order)
                product.amount -= 1  # зменшує кількість товару після вдалої покупки на 1
                await session.commit()
                # return {"message": "Product purchased successfully"}
                return {"You buy": f"{product.description}"}
            else:
                raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        return {"message": "you not auth"}

@router.post("/add_review/{product_id}")
async def add_review(
        product_id: int,
        review_text: str,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session)):
    product = await session.execute(select(Product).filter(Product.id == product_id))
    product = product.scalar()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Перевірте, чи користувач купив цей товар
    is_buyer = await session.execute(
        select(Order).filter(Order.buyer_id == current_user.id, Order.item_id == product.id))
    is_buyer = is_buyer.scalar()

    if not is_buyer:
        raise HTTPException(status_code=403, detail="Permission denied")

    review = Review(text=review_text, product_id=product_id, user_id=current_user.id)
    session.add(review)
    await session.commit()

    return {"message": "Review added successfully"}


@router.get("/get_reviews/{product_id}")
async def get_reviews(
        product_id: int,
        reviews_id: int,
        session: AsyncSession = Depends(get_async_session)):
    review = await session.execute(select(Review).where(Review.product_id == product_id, Review.id == reviews_id))
    review = review.scalar()
    if review is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"review": review.text, "user": review.user_id}
