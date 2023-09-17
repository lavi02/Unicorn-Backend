from pydantic import BaseModel
from typing import Union
from sqlalchemy import Column, String, Integer, JSON, ForeignKey, DateTime, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from src.database.users.user import UserTable
from src.database.stores.store import StoreTable
from src.database.stores.tables.table import StoreTableData
from src.database.stocks.stock import StocksTable
import pytz
from datetime import datetime

Base = declarative_base()


class CartTable(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey(UserTable.user_id), nullable=False)
    store_code = Column(String(50), ForeignKey(
        StoreTable.store_code), nullable=False)
    table_number = Column(String(50), nullable=False)
    stock_id = Column(String(50), ForeignKey(
        StocksTable.stock_id), nullable=False)
    stock_price = Column(Integer, ForeignKey(
        StocksTable.stock_price), nullable=False)
    stock_count = Column(Integer, nullable=False)
    stock_option = Column(JSON, nullable=True)
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))
    __table_args__ = (
        ForeignKeyConstraint(['store_code', 'table_number'],
                             [StoreTableData.store_code, StoreTableData.table_number]),
    )


class Cart(BaseModel):  # 장바구니
    user_id: Union[str, None] = None
    table_number: str
    product_id: str
    product_price: int
    product_count: int
    product_option: Union[dict, None] = None
