from pydantic import BaseModel
from sqlalchemy import Column, String, inspect, ForeignKey, Text

from .__conn__ import *

class StoreTable(Base):
    __tablename__ = 'store'
    store_code = Column(String(50), nullable=False)
    store_name = Column(String(50), nullable=False)

class StoreUserTable(Base):
    __tablename__ = 'store_user'
    store_code = Column(String(50), ForeignKey("store.store_code"), nullable=False)
    user_id = Column(String(50), primary_key=True, nullable=False)
    user_pw = Column(Text, nullable=False) # 비밀번호
    user_email = Column(String(50), nullable=False) # 이메일
    user_phone = Column(String(50), nullable=False) # 전화번호

class Store(BaseModel):
    store_code: str
    store_name: str

class StoreUser(BaseModel):
    store_code: str
    user_id: str
    user_pw: str
    user_email: str
    user_phone: str

# CartTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>

inspector = inspect(conn.engineData())
if not inspector.has_table('store'):
    StoreTable.__table__.create(bind=conn.engineData())
if not inspector.has_table('store_user'):
    StoreUserTable.__table__.create(bind=conn.engineData())