from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
import pytz
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from src.database.stores.store import StoreTable
from src.database.stocks.stock import StocksTable

Base = declarative_base()


class StoreLogTable(Base):
    __tablename__ = 'store_logs'
    store_code = Column(String(50), ForeignKey(
        StoreTable.store_code), nullable=False)
    stock_id = Column(String(50), ForeignKey(
        StocksTable.stock_id), nullable=False)
    stock_count = Column(Integer, nullable=False)
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))


class Store(BaseModel):
    store_code: str
    store_name: str
    store_status: bool = True
