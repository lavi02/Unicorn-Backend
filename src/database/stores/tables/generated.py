from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKeyConstraint, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.database.stores.tables.table import StoreTableData
import pytz
from datetime import datetime

Base = declarative_base()


class GeneratedTable(Base):
    __tablename__ = 'generated'
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_code = Column(String(50), nullable=False)
    table_number = Column(String(50), nullable=False)
    is_valid = Column(Boolean, nullable=False, default=True)
    generated_time = Column(DateTime, primary_key=True, default=datetime.now(
        pytz.timezone('Asia/Seoul')))
    __table_args__ = (
        ForeignKeyConstraint(
            ['store_code', 'table_number'],
            [StoreTableData.store_code, StoreTableData.table_number]
        ),
    )


class Generated(BaseModel):
    table_number: str
    is_valid: bool = True
    generated_time: datetime = datetime.now(pytz.timezone('Asia/Seoul'))
