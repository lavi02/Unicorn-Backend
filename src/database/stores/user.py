from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from src.database.stores.store import StoreTable

Base = declarative_base()


class StoreUserTable(Base):
    __tablename__ = 'store_user'
    store_code = Column(String(50), ForeignKey(
        StoreTable.store_code), nullable=False)
    user_id = Column(String(50), primary_key=True, nullable=False)
    user_name = Column(String(50), nullable=False)
