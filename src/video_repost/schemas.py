from pydantic import BaseModel

class RepostCreate(BaseModel):
    video_id: int
    to_user: int
