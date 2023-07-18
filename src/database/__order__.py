from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, inspect, JSON, Boolean, Integer

from .__conn__ import *

# store order table
class OrderTable(Base):
    __tablename__ = 'order'
    user_id = Column(String(50), nullable=False)
    store_code = Column(String(50), nullable=False)
    table_number = Column(String(50), nullable=False)
    product_id = Column(String(50), primary_key=True, nullable=False)
    product_price = Column(Integer, nullable=False)
    product_count = Column(Integer, nullable=False)
    product_option = Column(JSON, nullable=True)
    product_status = Column(Boolean, nullable=False, default=False)

class Order(BaseModel):
    store_code: str
    table_number: str
    product_id: str
    product_price: int
    product_count: int
    product_option: Union[dict, None] = None
    product_status: bool

# CartTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>

inspector = inspect(conn.engineData())
if not inspector.has_table('order'):
    OrderTable.__table__.create(bind=conn.engineData())