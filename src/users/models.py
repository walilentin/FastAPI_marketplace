from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import MetaData, Column, String, Boolean, TIMESTAMP, Integer, ForeignKey, Float, JSON, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from src.database import Base

metadata = MetaData()

class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)

    users = relationship("User", back_populates="role")

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    oauth_accounts = relationship("OAuthAccount", lazy="joined")
    balance = Column(Float, default=0.0)

    orders = relationship("Order", foreign_keys="[Order.buyer_id]", back_populates="buyer")
    comments = relationship("Comment", back_populates="user")
    videos = relationship("Video", back_populates="user")
    role = relationship("Role", back_populates="users", lazy="joined")