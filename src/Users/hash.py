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

def verify(plain: str, hashed: str) -> bool:
    """
    비밀번호 검증

    Args:
        plain (str): 평문
        hashed (str): 해시된 비밀번호

    Returns:
        bool: 검증 결과
    """
    return pwd_context.verify(plain, hashed)

def generateHash(password):
    return pwd_context.hash(password)

def auth(user_id: str, password: str):
    try:
        hasedPassword = generateHash(password)
        user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id, user_pw=hasedPassword).first()
        if not user:
            return False
        if not verify(password, user.user_pw):
            return False
        return user
    except Exception as e:
        return False

class redisData:
    def __init__(self, conn: redis.StrictRedis):
        self.conn = conn
    
    def setData(self, key: str, value: str, expireDate: int):
        return self.conn.setex(name=key, value=value, time=expireDate)
    
    def getData(self, key: str):
        return self.conn.get(key)
    
    def deleteData(self, key: str):
        return self.conn.delete(key)