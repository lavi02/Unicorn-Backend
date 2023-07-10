from os import urandom
from typing import Union
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.__conn__ import *
from src.database.__user__ import *

from src.settings.dependency import *

secret_key = urandom(24)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

def verify(plain, hashed) -> bool:
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

