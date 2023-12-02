from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.config import google_oauth_client, SECRET_AUTH
from src.users.base_config import auth_backend, fastapi_users
from src.pages.router import router as pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="/home/valik/FastAPI_marketplace/src/static"), name="static")
app.include_router(pages_router)

app.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET_AUTH,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["Auth"]
)

