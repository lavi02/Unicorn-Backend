from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, JSON, Integer, ForeignKey, DateTime, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from src.database.users.user import UserTable
from src.database.stores.store import StoreTable
from src.database.stores.tables.table import StoreTableData
from src.database.stocks.stock import StocksTable
import pytz
from datetime import datetime


Base = declarative_base()

class OrderTable(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey(UserTable.user_id), nullable=False)
    store_code = Column(String(50), nullable=False)
    table_number = Column(String(50), nullable=False)
    stock_id = Column(String(50), ForeignKey(
        StocksTable.stock_id), nullable=False)
    stock_price = Column(Integer, ForeignKey(
        StocksTable.stock_price), nullable=False)
    stock_count = Column(Integer, nullable=False)
    stock_option = Column(JSON, nullable=True)
    order_status = Column(Integer, nullable=False,
                          default=0)  # 0 처리중 1 처리완료 2 취소
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))
    __table_args__ = (
        ForeignKeyConstraint(
            ['store_code', 'table_number'],
            [StoreTableData.store_code, StoreTableData.table_number]
        ),
    )


class Order(BaseModel):
    store_code: str
    table_number: str
    stock_id: str
    stock_price: int
    stock_count: int
    stock_option: Union[dict, None] = None
    order_status: int = 0
