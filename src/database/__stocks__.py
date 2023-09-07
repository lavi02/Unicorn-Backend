from pydantic import BaseModel
from typing import Union, List
from sqlalchemy import ( 
    Column, String, inspect, 
    ForeignKey, Text, JSON,
    Integer, Boolean )
from sqlalchemy.orm import relationship

from .__conn__ import *

class StockImages(Base):
    __tablename__ = 'stock_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String(50), ForeignKey("stocks.stock_id"))
    image = Column(String(255), nullable=False)
    stock = relationship("StocksTable", back_populates="stock_images")

class StocksTable(Base):
    __tablename__ = 'stocks'
    store_code = Column(String(50),ForeignKey("store.store_code"), nullable=False)
    stock_name = Column(String(50), nullable=False)
    stock_id = Column(String(50), nullable=False, primary_key=True)
    stock_price = Column(String(50), nullable=False)
    stock_description = Column(Text, nullable=True)
    stock_option = Column(JSON, nullable=True)
    stock_category = Column(String(50), nullable=True)
    stock_images = relationship("StockImages", back_populates="stock")
    stock_status = Column(String(50), nullable=False, default="판매중")
    

class Stocks(BaseModel):
    store_code: str
    stock_name: str
    stock_id: Union[str, None] = None
    stock_price: str
    stock_description: Union[str, None] = None
    stock_option: Union[dict, None] = None
    stock_category: Union[str, None] = None
    stock_images: List[str] = []

# CartTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>

inspector = inspect(conn.engineData())
if not inspector.has_table('stocks'):
    StocksTable.__table__.create(bind=conn.engineData())
if not inspector.has_table('stock_images'):
    StockImages.__table__.create(bind=conn.engineData())