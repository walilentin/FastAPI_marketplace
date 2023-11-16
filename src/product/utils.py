from http.client import HTTPException
from src.product.models import Order


async def check_buyer_has_ordered(current_user, seller_id, session):
    order = session.query(Order).filter(Order.buyer_id == current_user.id, Order.seller_id == seller_id).first()

    if not order:
        raise HTTPException(status_code=400, detail="Buyer has not ordered from this seller")