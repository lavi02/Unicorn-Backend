from os import urandom
import redis

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.__conn__ import *
from src.database.__user__ import *

from src.settings.dependency import *

secret_key = urandom(24)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class hashData():
    @staticmethod
    def verify_password(plain, hashed):
        return pwd_context.verify(plain, hashed)
    
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

class redisData:
    def __init__(self, conn: redis.StrictRedis):
        self.conn = conn
    
    def setData(self, key: str, value: str, expireDate: int):
        return self.conn.setex(name=key, value=value, time=expireDate)
    
    def getData(self, key: str):
        return self.conn.get(key)
    
    def deleteData(self, key: str):
        return self.conn.delete(key)