from sqlalchemy import Column, String, Integer, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

metadata = MetaData()

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    video_id = Column(Integer, ForeignKey('video.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    video = relationship("Video", back_populates="comments")
    user = relationship("User", back_populates="comments")