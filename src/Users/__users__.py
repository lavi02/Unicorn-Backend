from fastapi.responses import JSONResponse, Response

from src.database.__conn__ import conn
from src.database.__user__ import UserTable, User
from src.settings.dependency import *
from src.Users.hash import *
from src.Users.__crud__ import UserCommands

from src.settings.dependency import app, sessionFix

redisSession = redisData(conn.redisConnect("session"))

@app.get(
        "/api/v1/user/list", description="유저 목록 조회",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def users():
    with sessionFix() as session:
        userData = UserCommands().read(session, UserTable)
        userList = []
        for user in userData:
            userList.append({
                "user_name": user.user_name,
                "user_id": user.user_id,
                "user_email": user.user_email,
                "user_phone": user.user_phone
            })
        return JSONResponse(status_code=200, content={"message": "success", "data": userList})
    
@app.post(
        "/api/v1/user/refresh", description="유저 토큰 갱신",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
)
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")
    except JWTError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")

    with sessionFix() as session:
        user = UserCommands().read(session, UserTable, id=user_id)
        if user is None:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Could not validate credentials")
        if redisSession.getData(user_id+"_refresh_token").decode("utf-8") != refresh_token:
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
        "/api/v1/user/token", description="유저 토큰 조회",
        tags=["user"]
    )
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        with sessionFix() as session:
            user = UserCommands().read(session, UserTable, id=form_data.username)
            if user is None:
                return { "message": "유저가 존재하지 않습니다." }
            isUser = hashData.verify_password(form_data.password, user.user_pw)
            if isUser:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = hashData.create_user_token(
                    data={"sub": user.user_id}, expires_delta=access_token_expires
                )

                refreshToken = hashData.create_refresh_token(user_id=user.user_id)
                if redisSession.setData(form_data.username, str(access_token), 600):
                    if redisSession.setData(form_data.username+"_refresh_token", str(refreshToken), 86400):
                        return {"access_token": access_token, "refresh_token": refreshToken}
                    else:
                        redisSession.deleteData(form_data.username)
                        redisSession.deleteData(form_data.username+"_refresh_token")
                        
                        return {"message": "redis error"}

                else:
                    return {"message": "redis error"}
            else:
                return {"message": "비밀번호가 일치하지 않습니다."}
    except Exception as e:
        return {"message": str(e)}

@app.get("/api/v1/user/login", description="유저 로그인", tags=["user"])
async def login(id: str, pw: str):
    form_data = OAuth2PasswordRequestForm(username=id, password=pw)
    try:
        response = await token(form_data)
        if "access_token" in response and "refresh_token" in response:
            return JSONResponse(status_code=200, content={"message": "success", "data": response})
        else:
            return JSONResponse(status_code=400, content={"message": "Failed to generate tokens"})
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


# json 형식으로 데이터를 받아올 때는 request body에 데이터를 넣어서 보내야 한다.
# json 형식으로 데이터를 보낼 때는 json.dumps()를 사용한다.
@app.post(
        "/api/v1/user/register", description="유저 등록", response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def create(user: User):
    try:
        with sessionFix() as session:
            # 비밀번호 해싱
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
            UserCommands().create(session, new_user)
            return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        raise JSONResponse(status_code=400, content={"message": str(e)})
    
@app.put(
        "/api/v1/user/update", description="유저 정보 수정", response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def update(user: User):
    with sessionFix() as session:
        update_user = UserCommands().read(session, UserTable, id=user.user_id)

        update_user.user_name = user.user_name
        update_user.user_id = user.user_id
        update_user.user_pw = user.user_pw
        update_user.user_email = user.user_email
        update_user.user_phone = user.user_phone

        result = UserCommands().update(session, UserTable, update_user)
        return JSONResponse(status_code=200, content={"message": result})
    
@app.delete(
        "/api/v1/user/delete", description="유저 삭제", response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["user"]
    )
async def delete(user_id: str):
    try:
        with sessionFix() as session:
            result = UserCommands().delete(session, UserTable, user_id)
            return JSONResponse(status_code=200, content={"message": result})
    # 세션 없을 때
    except HTTPException as e:
        if HTTPException.status_code == 401:
            return JSONResponse(status_code=401, content={"message": "unauthorized"})
        else:
            return JSONResponse(status_code=400, content={"message": str(e)})
    

@app.get(
        "/api/v1/user/logout", description="유저 로그아웃",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["user"]
    )
async def logout(sessionUID: Annotated[User, Depends(getCurrentUser)]):
    try:
        # redis에서도 삭제
        redisSession.deleteData(sessionUID.username)

        return JSONResponse(status_code=200, content={"message": "success"})
    except HTTPException as e:
        if HTTPException.status_code == 401:
            return JSONResponse(status_code=401, content={"message": "unauthorized"})
        else:
            return JSONResponse(status_code=400, content={"message": str(e)})

# check session
@app.get(
        "/api/v1/user/check", description="세션 확인",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "True" },
            400: { "description": "False" }
        }, tags=["develop"]
    )
async def check(sessionUID: Annotated[User, Depends(getCurrentUser)]):
    try:
        # redis에 없으면 세션에서도 삭제
        if not redisSession.getData(sessionUID.username):
            try:
                return JSONResponse(status_code=401, content={"message": "session not found"})
            except Exception as e:
                return JSONResponse(status_code=400, content={"message": str(e)})
        else:
            # uid64 쿠키값 공개
            return JSONResponse(status_code=200, content={"message": True})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})