from http.client import HTTPException
from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.router import templates
from src.database import get_async_session
from src.product.models import Product, Order, Review, Category
from src.product.schemas import ProductCreate
from src.users.base_config import fastapi_users, current_user_has_permission
from src.users.manager import get_user_manager
from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(prefix="/product")
<<<<<<< HEAD
category_router = APIRouter(prefix="/category")


@category_router.get("/{category_id}")
async def view_category(
        request: Request,
        category_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    category = await session.execute(select(Category).filter(Category.id == category_id))
    category = category.scalar()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    products = await session.execute(select(Product).filter(Product.category_id == category_id))
    products = products.scalars().all()

    return templates.TemplateResponse("category.html", {"request": request, "current_category": category, "product": products})

=======
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf


@router.post("/add_product", dependencies=[Depends(current_user_has_permission("create_product"))])
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


<<<<<<< HEAD
=======

>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
@router.delete("/delete-product/{product_id}", dependencies=[Depends(current_user_has_permission("delete_product"))])
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

<<<<<<< HEAD

=======
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
@router.post("/buy-product/{product_id}", dependencies=[Depends(current_user_has_permission("buy_product"))])
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


<<<<<<< HEAD
@router.post("/add-review/{product_id}", dependencies=[Depends(current_user_has_permission("add_review"))])
async def add_review(
        product_id: int,
        review_text: str,
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
        session: AsyncSession = Depends(get_async_session)
):
=======

@router.post("/add-review/{product_id}", dependencies=[Depends(current_user_has_permission("add_review"))])
async def add_review(
    product_id: int,
    review_text: str,
    current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
    session: AsyncSession = Depends(get_async_session)
):

>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
    product = await session.execute(select(Product).filter(Product.id == product_id))
    product = product.scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

<<<<<<< HEAD
=======

>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
    is_buyer = await session.execute(
        select(Order).filter(Order.buyer_id == current_user.id, Order.item_id == product.id)
    )
    is_buyer = is_buyer.scalar()
    if not is_buyer:
        raise HTTPException(status_code=403, detail="User is not a buyer of the product")

<<<<<<< HEAD
=======

>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
    review = Review(text=review_text, product_id=product_id, user_id=current_user.id)
    session.add(review)
    await session.commit()

    return {"message": "Review added successfully"}


@router.get("/get-reviews/{product_id}")
async def get_reviews(
        product_id: int,
        session: AsyncSession = Depends(get_async_session)):
    reviews = await session.execute(select(Review).where(Review.product_id == product_id))

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for the specified product")

    reviews_list = [{"review": review.text, "user": review.user_id} for review in reviews]
    return {"reviews": reviews_list}


<<<<<<< HEAD
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Category).where(Category.id >= 1)
    result = await session.execute(stmt)
    categories = result.scalars()
    category_list = [{"id": category.id, "name": category.name_category} for category in categories]
    return category_list


=======
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
@router.get("/search")
async def search(query: str, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(Product).where(func.lower(Product.name).ilike(f"%{query.lower()}%"))

        result = await session.execute(stmt)
        products = result.scalars().unique().all()

<<<<<<< HEAD
        product_list = [{"product": {"id": product.id, "name": product.name, "description": product.description,
                                     "price": product.price}} for product in products]

        return ({"query": query, "results": product_list})
=======
        product_list = [{"product": {"id": product.id, "name": product.name, "description": product.description, "price": product.price}} for product in products]

        return({"query": query, "results": product_list})
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

<<<<<<< HEAD

@router.get("/{product_id}")
async def view_product(
        request: Request,
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
=======
@router.get("/{product_id}")
async def view_product(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True)),
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
):
    product = await session.execute(select(Product).filter(Product.id == product_id))
    product = product.scalar()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

<<<<<<< HEAD
    return templates.TemplateResponse("product.html", {"request": request, "product": product, "user": current_user})
=======
    return templates.TemplateResponse("product.html", {"request": request, "product": product, "user": current_user})
>>>>>>> 5dec6267f8043cb818063b9fb8a5e0a8df7c1aaf
