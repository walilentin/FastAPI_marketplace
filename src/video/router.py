from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi.responses import StreamingResponse
from src.database import get_async_session
from src.users.base_config import fastapi_users
from src.users.manager import get_user_manager
from src.video.models import Video

video = APIRouter(prefix="/video")


@video.post("/upload")
async def upload_video(
        title: str = Form(...),
        video_file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: get_user_manager = Depends(fastapi_users.current_user(active=True, optional=True))
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="You must be logged in to upload videos")

    # Перевірка розширення файлу
    if not video_file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only .mp4 files are allowed")

    # Отримати дані з файлу
    file_data = await video_file.read()
    # Створити новий об'єкт Video та зберегти його в базу даних
    new_video = Video(title=title, video=file_data, user_id=current_user.id)

    session.add(new_video)
    await session.commit()

    return {"status": "success"}


@video.get("/{video_id}")
async def display_video(video_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        # Знайти відео за ідентифікатором
        video = await session.execute(select(Video).filter(Video.id == video_id))
        video = video.scalar()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        # Створити генератор для передачі даних частинами
        def generate_video():
            yield video.video

        # Повернути відео як потік
        return StreamingResponse(content=generate_video(), media_type="video/mp4")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
