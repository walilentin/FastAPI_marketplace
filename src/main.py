from fastapi import FastAPI
from src.config import google_oauth_client, SECRET_AUTH
from src.users.base_config import auth_backend, fastapi_users
from src.users.schemas import UserRead, UserCreate
from src.video.router import video as video_router
from src.comment.router import comment as comment_router
from src.video_repost.router import router as video_repost
from src.routers import router as page_router
from src.product.router import router as product_router
from src.users.router import router as user_router
from src.basket.router import router as basket_router

app = FastAPI()

app.include_router(basket_router)
app.include_router(video_router)
app.include_router(comment_router)
app.include_router(video_repost)
app.include_router(page_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET_AUTH,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)
