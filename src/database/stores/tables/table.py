from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from src.database.stores.store import StoreTable

Base = declarative_base()


class StoreTableData(Base):
    __tablename__ = 'store_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_code = Column(String(50), ForeignKey(
        StoreTable.store_code), nullable=False)
    table_number = Column(String(50), nullable=False)
    is_valid = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        Index('idx_storecode_tablenumber', 'store_code', 'table_number'),
    )


class StoreData(BaseModel):
    store_code: str
    table_number: str
    is_valid: bool = True
