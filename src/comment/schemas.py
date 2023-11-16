from pydantic import BaseModel

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    video_id: int
    user_id: int


