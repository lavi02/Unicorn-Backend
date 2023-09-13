from pydantic import BaseModel
from sqlalchemy import Column, String, inspect, Text
from typing import Union

from .__conn__ import *

class UserTable(Base): # 유저 테이블
    __tablename__ = 'user' #테이블 이름
    user_name = Column(String(50), nullable=False) # 이름
    user_id = Column(String(50), primary_key=True, nullable=False) # 아이디
    user_pw = Column(Text, nullable=False) # 비밀번호
    user_email = Column(String(50), nullable=False) # 이메일
    user_phone = Column(String(50), nullable=False) # 전화번호

class User(BaseModel): # 유저
    user_name: Union[str, None] = None
    user_id: str
    user_pw: Union[str, None] = None
    user_email: Union[str, None] = None
    user_phone: Union[str, None] = None
    is_valid: Union[bool, None] = None


# UserTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>


inspector = inspect(conn.engineData())
if not inspector.has_table('user'):
    UserTable.__table__.create(bind=conn.engineData())