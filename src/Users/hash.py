from os import urandom
import redis

from passlib.hash import oracle10
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.__conn__ import *
from src.database.__user__ import *

from src.settings.dependency import *

secret_key = urandom(32)
hashCode = "Hello_neighbor"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class hashData():
    @staticmethod
    def verify_password(plain, hashed):
        return oracle10.verify(hashCode, hashed, plain)
    
    @staticmethod
    def get_password_hash(password):
        return oracle10.hash(hashCode, password)

class redisData:
    def __init__(self, conn: redis.StrictRedis):
        self.conn = conn
    
    def setData(self, key: str, value: str, expireDate: int):
        return self.conn.setex(name=key, value=value, time=expireDate)
    
    def getData(self, key: str):
        return self.conn.get(key)
    
    def deleteData(self, key: str):
        return self.conn.delete(key)