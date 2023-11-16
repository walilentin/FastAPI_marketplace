from fastapi import UploadFile
from pydantic import BaseModel
from typing import Union

class VideoUpload(BaseModel):
    title: str
    video: Union[bytes, UploadFile]