from src.database.__conn__ import conn
from src.database.__user__ import UserTable, User
from src.Users.hash import *

from src.settings.dependency import app

@app.get("/api/v1/user/list")
async def users():
    users = conn.rdsSession().query(UserTable).all()
    return users

@app.get("/api/v1/user/login")
async def login(user_id: str, user_pw: str):
    try:
        user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id, user_pw=user_pw).first()
        if user:
            return {"message": "success"}
        else:
            return {"message": f"{user_id} is not found"}
    except Exception as e:
        return {"message": str(e)}

# json 형식으로 데이터를 받아올 때는 request body에 데이터를 넣어서 보내야 한다.
# json 형식으로 데이터를 보낼 때는 json.dumps()를 사용한다.
@app.post("/api/v1/user/register")
async def create(user: User):
    try:
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
        return {"message": str(e)}
    
@app.put("/api/v1/user/update")
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
        return {"message": str(e)}
    
@app.delete("/api/v1/user/delete")
async def delete(user_id: str):
    try:
        delete_user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id).first()
        conn.rdsSession().delete(delete_user)
        conn.rdsSession().commit()
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}
    
async def isCurrentUser(token: Annotated[str, Depends(oauth2)], user_id: str, password: str):
    credentialException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentialException
        token_data = TokenData(username=username)
    except JWTError:
        raise credentialException
    hasedPassword = generateHash(password)
    user = conn.rdsSession().query(UserTable).filter_by(user_id=user_id, user_pw=hasedPassword).first()


# get AccessToken
@app.post("/api/v1/user/token", response_model=Token)
async def loginForAccessToken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    