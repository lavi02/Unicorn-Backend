from fastapi.responses import JSONResponse, Response

from src.database.__conn__ import conn
from src.database.__user__ import UserTable, User
from src.settings.dependency import *
from src.Users.hash import *

from src.settings.dependency import app

class sessionData(BaseModel):
    user_id: str

cookie_params = CookieParameters()
backend = InMemoryBackend[UUID, sessionData]()
redisSession = redisData(conn.redisConnect("session"))

cookie = SessionCookie(
    cookie_name="uid64",
    identifier="general_verifier",
    auto_error=True,
    secret_key=secret_key,
    cookie_params=cookie_params
)
async def save_cookie(response: JSONResponse):
    await response

class verifySession(SessionVerifier[UUID, sessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, sessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: sessionData) -> bool:
        """
        If the session exists, it is valid
        """
        return True
    
verifySessionResult = verifySession(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=401, detail="Unauthorized")
)
        

@app.get(
        "/api/v1/user/list", description="유저 목록 조회",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def users():
    users = conn.rdsSession().query(UserTable).all()
    return users

@app.get(
        "/api/v1/user/login", description="유저 로그인",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def login(user_id: str, user_pw: str):
    try:
        sessionUID = uuid4()

        
        user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id).first()
        if user is None:
            return {"message": f"{user_id} is not found"}
        
        # password hash 검증
        # id가 localplayer0, password가 test2인 경우도 로그인 가능
        hashed_user_pw = hashData.get_password_hash(user_pw)
        isUser = True if user_id == "localplayer0" and user.user_pw == user_pw \
            else hashData.verify_password(user_pw, user.user_pw)
        if isUser:
            result = sessionData(user_id=user_id)
            await backend.create(sessionUID, result)

            # redis에도 저장. expired 하루. 문자열로 result 저장
            strUID = str(sessionUID)
            if redisSession.setData(strUID, user_id, 86400):

                response = JSONResponse({"message": "success"})
                cookie.attach_to_response(response, sessionUID)

                return response

            else:
                return {"message": "redis error"}
        else:
            return {"message": "password is not correct"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

# json 형식으로 데이터를 받아올 때는 request body에 데이터를 넣어서 보내야 한다.
# json 형식으로 데이터를 보낼 때는 json.dumps()를 사용한다.
@app.post(
        "/api/v1/user/register", description="유저 등록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def create(user: User):
    try:
        # 비밀번호 해싱
        user.user_pw = hashData.get_password_hash(user.user_pw)
        session = conn.rdsSession()

        new_user = UserTable(
            user_name=user.user_name,
            user_id=user.user_id,
            user_pw=user.user_pw,
            user_email=user.user_email,
            user_phone=user.user_phone
        )
        session.add(new_user)
        session.commit()

        return {"message": "success", "data": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put(
        "/api/v1/user/update", description="유저 정보 수정",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["user"]
    )
async def update(user: User):
    try:
        update_user = conn.rdsSession().query(UserTable).filter_by(id=user.id).first()

        update_user.user_name = user.user_name
        update_user.user_id = user.user_id
        update_user.user_pw = user.user_pw
        update_user.user_email = user.user_email
        update_user.user_phone = user.user_phone
        conn.rdsSession().commit()
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete(
        "/api/v1/user/delete", description="유저 삭제",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["user"]
    )
async def delete(user_id: str):
    try:
        delete_user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id).first()
        conn.rdsSession().delete(delete_user)
        conn.rdsSession().commit()
        return {"message": "success"}
    
    # 세션 없을 때
    except HTTPException as e:
        if HTTPException.status_code == 401:
            return {"message": "unauthorized"}
        else:
            HTTPException(status_code=400, detail=str(e))
    

@app.get(
        "/api/v1/user/logout", description="유저 로그아웃",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["user"]
    )
async def logout(response: Response, sessionUID: UUID = Depends(cookie)):
    try:
        await backend.delete(sessionUID)
        cookie.delete_from_response(response)

        # redis에서도 삭제
        redisSession.deleteData(str(sessionUID))

        return {"message": "success"}
    except HTTPException as e:
        if HTTPException.status_code == 401:
            return {"message": "unauthorized"}
        else:
            HTTPException(status_code=400, detail=str(e))
    

# check session
@app.get(
        "/api/v1/user/check", description="세션 확인",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "True" },
            400: { "description": "False" }
        }, tags=["develop"]
    )
async def check(sessionUID: UUID = Depends(cookie)):
    try:
        await backend.read(sessionUID)

        # redis에 없으면 세션에서도 삭제
        if not redisSession.getData(str(sessionUID)):
            try:
                await backend.delete(sessionUID)

                return {"message": "True"}
            except Exception as e:
                return HTTPException(status_code=401, detail="session not found")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))