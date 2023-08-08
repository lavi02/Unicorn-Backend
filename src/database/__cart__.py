from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, inspect, Integer, JSON

from .__conn__ import *

class CartTable(Base): # 장바구니 테이블
    __tablename__ = 'cart' #테이블 이름
    user_id = Column(String(50), nullable=False) # 아이디
    table_number = Column(String(50), nullable=False) # 테이블 번호
    product_id = Column(String(50), primary_key=True, nullable=False) # 상품 아이디
    product_price = Column(Integer, nullable=False) # 상품 가격
    product_count = Column(Integer, nullable=False) # 상품 개수
    product_option = Column(JSON, nullable=True) # 상품 옵션

class Cart(BaseModel): # 장바구니
    user_id: Union[str, None] = None
    table_number: str
    product_id: str
    product_price: int
    product_count: int
    product_option: Union[dict, None] = None


# CartTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>


inspector = inspect(conn.engineData())
if not inspector.has_table('cart'):
    CartTable.__table__.create(bind=conn.engineData())