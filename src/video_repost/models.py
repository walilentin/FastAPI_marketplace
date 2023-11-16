from sqlalchemy import Column, Integer, MetaData, ForeignKey
from src.database import Base

metadata = MetaData()

class Repost(Base):
    __tablename__ = "repost"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', use_alter=True), nullable=False)
    video_id = Column(Integer, ForeignKey('video.id', use_alter=True), nullable=False)
    to_user = Column(Integer, ForeignKey('user.id', use_alter=True))
