from fastapi import status, Depends
from datetime import timedelta
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from src.services.util.hash import (
    hashData, secret_key, ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES, UserToken,
    jwt, JWTError, redisData, getCurrentUser
)
from src.database.__init__ import get_db, redis_client
from src.database.users.user import UserTable, User
from src.services.crud.users.user import UserCommands
from src.services.__init__ import app

#############################################################################################################


@app.post(
    "/api/v1/user/token", description="유저 토큰 조회",
    tags=["user"], name="유저 토큰 조회",
    include_in_schema=False
)
@inject
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session=Depends(get_db)):
    try:
        redisSession = redisData(redis_client)
        user = UserCommands().read(session=session, where=UserTable, id=form_data.username)
        if user is None:
            return {"message": "유저가 존재하지 않습니다."}
        isUser = hashData.verify_password(form_data.password, user.user_pw)
        if isUser:
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = hashData.create_user_token(
                data={"sub": user.user_id}, expires_delta=access_token_expires
            )

            refreshToken = hashData.create_refresh_token(user_id=user.user_id)
            if redisSession.setData(form_data.username, access_token, 600):
                if redisSession.setData(form_data.username+"_refresh_token", str(refreshToken), 86400):
                    return {"access_token": access_token, "refresh_token": refreshToken}
                else:
                    redisSession.deleteData(form_data.username)
                    redisSession.deleteData(
                        form_data.username+"_refresh_token")

                    return {"message": "redis error"}

            else:
                return {"message": "redis error"}
        else:
            return {"message": "비밀번호가 일치하지 않습니다."}
    except Exception as e:
        return {"message": str(e)}


@app.get(
    "/api/v1/user/list", description="유저 목록 조회",
    response_class=JSONResponse, tags=["user"],
    name="유저 목록 조회"
)
@inject
async def users(session=Depends(get_db)):
    try:
        userData = UserCommands().read(session=session, where=UserTable)
        userList = []

        if type(userData) == str:
            return JSONResponse(status_code=400, content={"message": userData})
        
        for user in userData:
            userList.append({
                "user_name": user.user_name,
                "user_id": user.user_id,
                "user_email": user.user_email,
                "user_phone": user.user_phone
            })
        return JSONResponse(status_code=200, content={"message": "success", "data": userList})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": "fail", "data": str(e)})


@app.get("/api/v1/user/login", description="유저 로그인", tags=["user"], name="유저 로그인")
async def login(id: str, pw: str):
    form_data = OAuth2PasswordRequestForm(username=id, password=pw)
    try:
        response = await token(form_data, get_db())
        if "access_token" in response and "refresh_token" in response:
            return JSONResponse(status_code=200, content={"message": "success", "data": response})
        else:
            return JSONResponse(status_code=400, content={"message": "Failed to generate tokens"})

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.get(
    "/api/v1/user/logout", description="유저 로그아웃",
    tags=["user"], name="유저 로그아웃"
)
@inject
async def logout(
    token: UserToken = Depends(getCurrentUser),
    session=Depends(get_db)
):
    try:
        sessionUID = await getCurrentUser(token=token, session=session)

        redisSession = redisData(redis_client)
        result = redisSession.deleteData(sessionUID.username)

        if result == 1:
            result = redisSession.deleteData(sessionUID.username+"_refresh_token")
            return JSONResponse(status_code=200, content={"message": "success"})
        else:
            return JSONResponse(status_code=401, content={"message": "unauthorized"})

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.get(
    "/api/v1/user/check", description="세션 확인",
    tags=["develop"], response_class=JSONResponse,
)
async def check(token: UserToken = Depends(getCurrentUser)):
    try:
        redisSession = redisData(redis_client)
        if not redisSession.getData(token.username):
            try:
                return JSONResponse(status_code=401, content={"message": "session not found"})
            except Exception as e:
                return JSONResponse(status_code=400, content={"message": str(e)})
        else:
            return JSONResponse(status_code=200, content={"message": True})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.post(
    "/api/v1/user/refresh", description="유저 토큰 갱신",
    response_class=JSONResponse, tags=["user"],
    name="유저 토큰 갱신"
)
@inject
async def refresh_access_token(refresh_token: str, session=Depends(get_db)):
    try:
        redisSession = redisData(redis_client)
        payload = jwt.decode(refresh_token, secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")
    except JWTError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")

    user = UserCommands().read(session=session, where=UserTable, id=user_id)
    if user is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")
    if redis_client.get(user_id+"_refresh_token").decode("utf-8") != refresh_token:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = hashData.create_user_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
    )

    if redisSession.getData(user_id):
        redisSession.deleteData(user_id)
        redisSession.setData(user_id, str(access_token), 600)
    else:
        redisSession.setData(user_id, str(access_token), 600)

    return JSONResponse(status_code=200, content={"access_token": access_token})


@app.post(
    "/api/v1/user/register", description="유저 등록", response_class=JSONResponse,
    tags=["user"], name="유저 등록"
)
@inject
async def create(user: User, session=Depends(get_db)):
    try:
        user.user_pw = hashData.get_password_hash(user.user_pw)
        if user.user_type == None:
            user.user_type = 0

        new_user = UserTable(
            user_name=user.user_name,
            user_id=user.user_id,
            user_pw=user.user_pw,
            user_email=user.user_email,
            user_type=user.user_type,
            user_phone=user.user_phone
        )
        result = UserCommands().create(session=session, target=new_user)
        print(result)
        if result == None:
            return JSONResponse(status_code=200, content={"message": "success"})
        else:
            return JSONResponse(status_code=400, content={"message": result})
    except Exception as e:
        raise JSONResponse(status_code=400, content={"message": str(e)})
