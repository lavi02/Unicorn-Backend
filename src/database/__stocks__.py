from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, inspect, ForeignKey, Text, JSON

from .__conn__ import *

class StocksTable(Base):
    __tablename__ = 'stocks'
    store_code = Column(String(50),ForeignKey("store.store_code"), nullable=False)
    stock_name = Column(String(50), nullable=False)
    stock_id = Column(String(50), nullable=False, primary_key=True)
    stock_price = Column(String(50), nullable=False)
    stock_description = Column(Text, nullable=True)
    stock_option = Column(JSON, nullable=True)
    

class Stocks(BaseModel):
    store_code: str
    stock_name: str
    stock_id: Union[str, None] = None
    stock_price: str
    stock_description: Union[str, None] = None
    stock_option: Union[dict, None] = None

# CartTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>

inspector = inspect(conn.engineData())
if not inspector.has_table('stocks'):
    StocksTable.__table__.create(bind=conn.engineData())