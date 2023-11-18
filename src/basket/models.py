from sqlalchemy import Column, Integer, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from src.database import Base

metadata = MetaData()

class Basket(Base):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", foreign_keys=[user_id], lazy="joined")
    product = relationship('Product', foreign_keys=[product_id], back_populates='baskets')
