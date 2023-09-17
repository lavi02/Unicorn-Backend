from os import urandom
import redis

from passlib.hash import oracle10
from datetime import datetime, timedelta, timezone
from typing import Union

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from dependency_injector.wiring import inject, Provide
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from src.database.__init__ import container, redis_client
from src.services.crud.users.user import UserCommands, UserTable

secret_key = urandom(32)
hashCode = "Hello_neighbor"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2Schema = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")


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
            expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
        else:
            expire = datetime.now(
                timezone(timedelta(hours=9))) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_id: str, expires_delta: Union[timedelta, None] = None):
        to_encode = {"sub": user_id}
        if expires_delta:
            expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
        else:
            expire = datetime.now(
                timezone(timedelta(hours=9))) + timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    @inject
    def verify_token(token: str, session: Session = Provide[container.SessionLocal]):
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


@inject
async def getCurrentUser(
    request: Request,
    session: Session = Provide[container.SessionLocal]
):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    user_token = hashData.verify_token(token, session)
    redisSession = redisData(redis_client)
    storedToken = redisSession.getData(user_token.username).decode("utf-8")
    try:
        if storedToken == token:
            return user_token
        else:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


class redisData:
    def __init__(self, conn: redis.StrictRedis):
        self.conn = conn

    def setData(self, key: str, value: str, expireDate: int):
        return self.conn.setex(name=key, value=value, time=expireDate)

    def getData(self, key: str):
        return self.conn.get(key)

    def deleteData(self, key: str):
        return self.conn.delete(key)

