from os import urandom
import redis

from passlib.hash import oracle10
from datetime import datetime, timedelta, timezone
from typing import Union
from typing_extensions import Annotated

from fastapi import Depends, HTTPException, status
from src.database.__conn__ import *
from src.database.__user__ import *
from src.Users.__crud__ import *

from src.settings.dependency import *

secret_key = urandom(32)
hashCode = "Hello_neighbor"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

class TokenData(BaseModel):
    access_token: str
    token_type: str

class UserToken(BaseModel):
    username: Union[str, None] = None
    token: Union[str, None] = None

class hashData():
    @staticmethod
    def verify_password(plain, hashed):
        return oracle10.verify(hashCode, hashed, plain)
    
    @staticmethod
    def get_password_hash(password):
        return oracle10.hash(hashCode, password)

    @staticmethod
    def create_user_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            # timezone seoul
            expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
        else:
            expire = datetime.now(timezone(timedelta(hours=9))) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(user_id: str, expires_delta: Union[timedelta, None] = None):
        to_encode = {"sub": user_id}
        if expires_delta:
            expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
        else:
            expire = datetime.now(timezone(timedelta(hours=9))) + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: Annotated[str, Depends(oauth2Schema)]):
        with sessionFix() as session:
            credentialsException = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise credentialsException
                token_data = UserToken(username=user_id, token=token)
            except JWTError:
                raise credentialsException
            
            user = UserCommands().read(session, UserTable, id=user_id)
            if user is None:
                raise credentialsException
            return token_data
        
async def getCurrentUser(
        token: Annotated[User, Depends(hashData().verify_token)]
    ):
    redisSession = redisData(conn.redisConnect("session"))
    storedToken = redisSession.getData(token.username).decode("utf-8")

    if storedToken == token.token:
        return token
    else:
        # 토큰만료 확인
        if storedToken is None:
            raise HTTPException(status_code=401, detail="Token expired")
        raise HTTPException(status_code=400, detail="Invalid token")

class redisData:
    def __init__(self, conn: redis.StrictRedis):
        self.conn = conn
    
    def setData(self, key: str, value: str, expireDate: int):
        return self.conn.setex(name=key, value=value, time=expireDate)
    
    def getData(self, key: str):
        return self.conn.get(key)
    
    def deleteData(self, key: str):
        return self.conn.delete(key)