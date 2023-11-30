from datetime import datetime
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseOAuthAccountTable,
)
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role_permissions = Column(JSON, default=[])

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
    is_verified = Column(Boolean, default=False, nullable=False)

    oauth_accounts = relationship("OAuthAccount", lazy="joined")
    balance = Column(Float, default=0.0)

    orders = relationship("Order", foreign_keys="[Order.buyer_id]", back_populates="buyer", lazy="joined")
    comments = relationship("Comment", back_populates="user")
    videos = relationship("Video", back_populates="user")

    role = relationship("Role", back_populates="users", lazy="joined")

    def get_filtered_info(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "registered_at": self.registered_at,
            "is_active": self.is_active,
            "balance": self.balance,
            "role": {
                "id": self.role.id,
                "name": self.role.name,
                "role_permissions": self.role.role_permissions,
            }
        }