from pydantic import BaseModel
from typing import Union, List
from sqlalchemy import (
    Column, String, ForeignKey,
    Text, JSON, Integer, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.database.stores.store import StoreTable

Base = declarative_base()


class StocksTable(Base):
    __tablename__ = 'stocks'
    id = Column(int, autoincrement=True, primary_key=True)
    store_code = Column(String(50), ForeignKey(
        StoreTable.store_code), nullable=False)
    stock_name = Column(String(50), nullable=False)
    stock_id = Column(String(50), nullable=False)
    stock_price = Column(Integer, nullable=False)
    stock_description = Column(Text, nullable=True)
    stock_option = Column(JSON, nullable=True)
    stock_category = Column(String(50), nullable=True)
    stock_images = relationship("StockImages", back_populates="stock")
    stock_status = Column(String(50), nullable=False, default="판매중")
    __table_args__ = (
        Index('idx_stockprice', 'stock_price'),
    )


class Stocks(BaseModel):
    id: int
    store_code: str
    stock_name: str
    stock_id: Union[str, None] = None
    stock_price: str
    stock_description: Union[str, None] = None
    stock_option: Union[dict, None] = None
    stock_category: Union[str, None] = None
    stock_images: List[str] = []
