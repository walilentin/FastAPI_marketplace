from fastapi import APIRouter, Request, Depends
from starlette.staticfiles import StaticFiles

from src.admin.router import templates
from src.users.base_config import current_user_optional, current_user_has_permission, fastapi_users, auth_backend
from src.users.models import User
from src.users.schemas import UserRead, UserCreate
from src.video.router import video as video_router
from src.comment.router import comment as comment_router
from src.video_repost.router import router as video_repost
from src.product.router import router as product_router
from src.basket.router import router as basket_router
from src.admin.router import router as admin_router

router = APIRouter(prefix="/v1")

router.mount("/static", StaticFiles(directory="/home/valik/Стільниця/FastAPI-like-TikTok/src/static"), name="static")

router.include_router(admin_router, tags=["Admin"])
router.include_router(basket_router,tags=["Basket"])
router.include_router(video_router,tags=["Video"])
router.include_router(comment_router,tags=["Comment"])
router.include_router(video_repost,tags=["Video_repost"])
router.include_router(product_router,tags=["Product"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"]
)

@router.get("/")
async def home(request: Request, current_user: User = current_user_optional()):
    return templates.TemplateResponse("base.html", {"request": request, "user": current_user})





@router.get("/account", dependencies=[Depends(current_user_has_permission("view_site"))])
async def account(request: Request, current_user: User = current_user_optional()):
    return templates.TemplateResponse("account.html", {"request": request, "user": current_user})