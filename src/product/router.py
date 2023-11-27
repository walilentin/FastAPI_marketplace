from http.client import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.product.models import Product, Order, Review, Category
from src.product.schemas import ProductCreate
from src.users.base_config import fastapi_users, current_user_buyer, current_user_guest, current_user_seller
from src.users.manager import get_user_manager
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("/add_product", dependencies=[Depends(current_user_seller)])
async def create_product(
        product: ProductCreate,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session),
):
    if current_user:
        category = await session.execute(select(Category).filter(Category.id == product.category_id))
        category = category.scalar()
        if category:
            stmt = Product(seller_id=current_user.id, **product.dict())
            session.add(stmt)
            await session.commit()
            return stmt
        else:
            raise HTTPException(status_code=404, detail="Category not found")
    else:
        return {"message": "you not auth"}



@router.delete("/delete-product/{product_id}", dependencies=[Depends(current_user_seller)])
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

        await session.execute(delete(Product).where(Product.id == product_id))
        await session.commit()

        return {"status": "success"}
    else:
        return {"message": "you not auth"}

@router.post("/buy-product/{product_id}")
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
            if current_user.balance >= product.price:
                order = Order(buyer_id=current_user.id, seller_id=product.seller_id, item_id=product.id)
                session.add(order)
                product.amount -= 1
                current_user.balance -= product.price
                await session.commit()
                # return {"message": "Product purchased successfully"}
                return {"You buy": f"{product.description}"}
            else:
                raise HTTPException(status_code=400, detail="Insufficient funds")
    else:
        return {"message": "you not auth"}

@router.post("/buy-product/{product_id}", dependencies=[Depends(current_user_buyer)])
async def buy_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    product = await session.execute(select(Product).filter(Product.id == product_id))
    product = product.scalar()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the buyer is the seller
    if current_user_buyer.id == product.seller_id:
        raise HTTPException(status_code=403, detail="Seller cannot buy their own product")

    # Check if the product is in stock
    if product.amount < 1:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    # Check if the buyer has sufficient funds
    if current_user_buyer.balance < product.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Perform the purchase
    order = Order(buyer_id=current_user_buyer.id, seller_id=product.seller_id, item_id=product.id)
    session.add(order)
    product.amount -= 1
    current_user_buyer.balance -= product.price
    await session.commit()

    return {"message": "Product purchased successfully"}



@router.post("/add-review/{product_id}", dependencies=[Depends(current_user_buyer)])
async def add_review(
    product_id: int,
    review_text: str,
    session: AsyncSession = Depends(get_async_session)
):
    product = await session.execute(select(Product).filter(Product.id == product_id))
    product = product.scalar()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    is_buyer = await session.execute(
        select(Order).filter(Order.buyer_id == current_user_buyer.id, Order.item_id == product.id)
    )
    is_buyer = is_buyer.scalar()

    review = Review(text=review_text, product_id=product_id, user_id=current_user_buyer.id)
    session.add(review)
    await session.commit()

    return {"message": "Review added successfully"}


@router.get("/get-reviews/{product_id}", dependencies=[Depends(current_user_guest)])
async def get_reviews(
        product_id: int,
        reviews_id: int,
        session: AsyncSession = Depends(get_async_session)):
    review = await session.execute(select(Review).where(Review.product_id == product_id, Review.id == reviews_id))
    review = review.scalar()
    if review is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"review": review.text, "user": review.user_id}
