from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, Text, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTable(Base):  # 유저 테이블
    __tablename__ = 'user'  # 테이블 이름
    user_name = Column(String(50), nullable=False)  # 이름
    user_id = Column(String(50), primary_key=True, nullable=False)  # 아이디
    user_pw = Column(Text, nullable=False)  # 비밀번호
    user_email = Column(String(50), nullable=False)  # 이메일
    user_type = Column(Integer, nullable=False, default=0)  # d
    user_phone = Column(String(50), nullable=False)  # 전화번호
    is_valid = Column(Boolean, nullable=False, default=True)


class User(BaseModel):  # 유저
    user_name: str
    user_id: str
    user_pw: str
    user_email: str
    user_type: int
    user_phone: str

class updateUser(BaseModel):  
    user_name: Union[str, None] = None
    user_pw: Union[str, None] = None
    user_email: Union[str, None] = None
    user_phone: Union[str, None] = None
    user_type: Union[int, None] = None
