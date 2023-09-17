from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StoreTable(Base):
    __tablename__ = 'store'
    store_code = Column(String(50), primary_key=True, nullable=False)
    store_name = Column(String(50), nullable=False)
    store_status = Column(Boolean, nullable=False, default=True)


class Store(BaseModel):
    store_code: str
    store_name: str
    store_status: bool = True
