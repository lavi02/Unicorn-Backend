from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from src.database.stocks.stock import StocksTable
from sqlalchemy.orm import relationship

Base = declarative_base()


class StockImages(Base):
    __tablename__ = 'stock_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String(50), ForeignKey(
        StocksTable.stock_id), nullable=False)
    image = Column(String(255), nullable=False)
    stock = relationship("StocksTable", back_populates="stock_images")


class Images(BaseModel):
    stock_id: str
    image: str
