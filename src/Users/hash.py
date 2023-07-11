from os import urandom
from typing import Union, Optional
from typing_extensions import Annotated

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.__conn__ import *
from src.database.__user__ import *

from src.settings.dependency import *

secret_key = urandom(24)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

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
    
def createAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    """
    토큰 생성

    Args:
        data (dict): 토큰에 담을 데이터
        expires_delta (Optional[timedelta], optional): 토큰 만료 시간. Defaults to None.

    Returns:
        [type]: [description]
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone('Asia/Seoul')) + expires_delta
    else:
        expire = datetime.now(timezone('Asia/Seoul')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt