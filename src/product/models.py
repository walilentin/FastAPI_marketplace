from datetime import datetime

from sqlalchemy import MetaData, Column, Integer, ForeignKey, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from src.database import Base

metadata = MetaData()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name_category = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    seller = relationship("User", foreign_keys=[seller_id], lazy="joined")
    orders = relationship("Order", back_populates="product", lazy="joined")
    category = relationship("Category", back_populates="products")
<<<<<<< HEAD
=======
    baskets = relationship("Basket", back_populates="product")
>>>>>>> 12d5085 (add basket)

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], lazy="joined")
    product = relationship("Product", foreign_keys=[product_id], lazy="joined")


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="orders", lazy="joined")
    seller = relationship("User", foreign_keys=[seller_id], lazy="joined")
    product = relationship("Product", lazy="joined")
