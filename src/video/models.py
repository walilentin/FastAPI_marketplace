from sqlalchemy import Column, String, Integer, MetaData, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from src.database import Base

metadata = MetaData()

class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    video = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="videos")
    comments = relationship("Comment", back_populates="video")
