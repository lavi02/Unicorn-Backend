from pydantic import BaseModel
from sqlalchemy import Column, String, inspect

from .__conn__ import *

class UserTable(Base): # 유저 테이블
    __tablename__ = 'user' #테이블 이름
    user_name = Column(String(50), nullable=False) # 이름
    user_id = Column(String(50), primary_key=True, nullable=False) # 아이디
    user_pw = Column(String(50), nullable=False) # 비밀번호
    user_email = Column(String(50), nullable=False) # 이메일
    user_phone = Column(String(50), nullable=False) # 전화번호

class User(BaseModel): # 유저
    user_name: str
    user_id: str
    user_pw: str
    user_email: str
    user_phone: str


# UserTable 테이블 생성
# 이미 생성되어있는지 확인 후 생성
# <class 'sqlalchemy.engine.base.Connection'>


inspector = inspect(conn.engineData())
if not inspector.has_table('user'):
    UserTable.__table__.create(bind=conn.engineData())
    print("테이블 생성 완료")
else:
    print("이미 테이블이 존재합니다.")