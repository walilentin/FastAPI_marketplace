from fastapi import FastAPI, Depends
from src.config import google_oauth_client, SECRET_AUTH
from src.users.base_config import auth_backend, fastapi_users, current_user_has_permission
from src.users.models import User
from src.users.schemas import UserRead, UserCreate
from src.video.router import video as video_router
from src.comment.router import comment as comment_router
from src.video_repost.router import router as video_repost
from src.product.router import router as product_router
from src.basket.router import router as basket_router
from src.admin.router import router as admin


app = FastAPI()


app.include_router(basket_router)
app.include_router(video_router)
app.include_router(comment_router)
app.include_router(video_repost)
app.include_router(product_router)
app.include_router(admin)
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


@app.get("/protected")
async def protected_route(user: User = Depends(current_user_has_permission("get_reviews"))):
    return {"message": "You have the required permission to access this route"}

@app.get("/another_protected")
async def another_protected_route(user: User = Depends(current_user_has_permission("delete_product"))):
    return {"message": "You have the required permission to access this route"}
