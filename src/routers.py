from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.users.manager import get_user_manager
from src.video.models import Video
from src.users.base_config import fastapi_users

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# @router.get("/")
# async def home(request: Request, session: AsyncSession = Depends(get_async_session),
#                current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))):
#     if current_user:
#         query = select(Video).where(Video.user_id == current_user.id)
#         video = await session.execute(query)
#         video = video.scalars()
#     else:
#         video = None
#     return templates.TemplateResponse("index.html", {"request": request, "user": current_user, "video": video})

#
# @router.get("/auth")
# async def read_auth(request: Request):
#     return templates.TemplateResponse("auth.html", {"request": request})
#
#
# @router.get("/registration")
# async def read_registration(request: Request):
#     return templates.TemplateResponse("registration.html", {"request": request})
