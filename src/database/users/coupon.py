from pydantic import BaseModel
from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.database.users.user import UserTable
import pytz
from datetime import datetime

Base = declarative_base()

class UserCoupon(Base):
    __tablename__ = 'coupon'
    user_id = Column(String(50), ForeignKey(UserTable.user_id),
                     primary_key=True, nullable=False)
    contents = Column(JSON, nullable=False)
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))


class Coupon(BaseModel):
    user_id: str
    contents: dict
    generated_time: datetime = datetime.now(pytz.timezone('Asia/Seoul'))
