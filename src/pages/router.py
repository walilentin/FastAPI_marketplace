from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.router import templates
from src.database import get_async_session
from src.product.models import Product
from src.users.base_config import current_user_has_permission, current_user
from src.users.models import User

router = APIRouter(prefix="/v1", tags=["Pages"])


@router.get("/", dependencies=[Depends(current_user_has_permission("view_site"))])
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/admin", dependencies=[Depends(current_user_has_permission("manage_users"))])
async def home(request: Request):
    return templates.TemplateResponse("admins.html", {"request": request})


@router.get("/account", dependencies=[Depends(current_user_has_permission("view_site"))])
async def home(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse("account.html", {"request": request, "user":user})

