import random
import string
from typing import List
from fastapi import Form, File, UploadFile
from fastapi.responses import JSONResponse

from src.database.__stocks__ import Stocks, StocksTable
from src.database.__store__ import Store, StoreTable, StoreUser, StoreUserTable
from src.stocks.store.__crud__ import StocksCommands
from src.settings.dependency import *

from src.Users.__users__ import *
from src.Users.hash import *

from src.settings.dependency import app, sessionFix

def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.sample(characters, length))
    return random_string

@app.post(
        "/api/v1/stocks/add", description="상품목록 추가",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["product"]
    )
async def addStocks(
    temp: Annotated[User, Depends(getCurrentUser)],
    store_code: str = Form(...),
    stock_name: str = Form(...),
    stock_price: str = Form(...),
    stock_description: str = Form(None),
    stock_option: dict = Form(None),
    stock_images: List[UploadFile] = File(...)
):
    try:
        with sessionFix() as session:
            stock_id = generate_random_string(24)
            imageUrls = []

            for file in stock_images:
                result = Uploader(file, f"/{store_code}/{stock_id}/{file.filename}")
                if result == "success":
                    imageUrls.append(f"/{store_code}/{stock_id}/{file.filename}")
                else:
                    return JSONResponse(status_code=400, content={"message": "cannot upload image to s3"})
            new_stock = StocksTable(
                store_code=store_code,
                stock_name=stock_name,
                stock_id=stock_id,
                stock_price=stock_price,
                stock_description=stock_description,
                stock_option=stock_option,
                stock_image=imageUrls
            )
            if StocksCommands().create(session, new_stock) == None:
                return JSONResponse(status_code=200, content={"message": "success", "stock_id": stock_id})
            else:
                return JSONResponse(status_code=400, content={"message": "fail"})
            
    except Exception:
        return JSONResponse(status_code=401, content={"message": "로그인이 필요합니다."})



# 장바구니 목록
@app.get(
        "/api/v1/stocks/list", description="특정 상점의 전체 상품 목록 & 특정 상품 조회",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["product"]
    )
async def stocksList(store_code: str, 
                    _: Annotated[User, Depends(getCurrentUser)], stock_id: Union[str, None] = None):
    try:
        with sessionFix() as session:
            stocks = StocksCommands().readStoreStocks(session, StocksTable, store_code=store_code, stock_id=stock_id)
            stocksList = []
            for i in stocks:
                stocksList.append({
                    "store_code": i.store_code,
                    "stock_name": i.stock_name,
                    "stock_id": i.stock_id,
                    "stock_price": i.stock_price,
                    "stock_description": i.stock_description,
                    "stock_option": i.stock_option
                })
            return JSONResponse(status_code=200, content={"message": "success", "stocks": stocksList})
    except Exception:
        return JSONResponse(status_code=401, content={"message": "로그인이 필요합니다."})
    
# 상품내용 변경
@app.put(
        "/api/v1/stocks/update", description="상품내용 변경",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["product"]
    )
async def updateStocks(stocks: Stocks, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            target = StocksTable(
                store_code=stocks.store_code,
                stock_name=stocks.stock_name,
                stock_id=stocks.stock_id,
                stock_price=stocks.stock_price,
                stock_description=stocks.stock_description,
                stock_option=stocks.stock_option,
            )
            if StocksCommands().updateStoreStocks(session, StocksTable, target) == None:
                return JSONResponse(status_code=200, content={"message": "success"})
            else:
                return JSONResponse(status_code=400, content={"message": "fail"})
            
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": "로그인이 필요합니다."})
    

# 상품 삭제
@app.delete(
        "/api/v1/stocks/delete", description="상품 삭제",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["product"]
    )
async def deleteStocks(store_code: str, stock_id, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            StocksCommands().deleteStocks(session, StocksTable, store_code=store_code, stock_id=stock_id)
            return JSONResponse(status_code=200, content={"message": "success"})
    except Exception:
        return JSONResponse(status_code=401, content={"message": "로그인이 필요합니다."})


# store_code = generate_random_string(24)
# 상점 추가
@app.post(
        "/api/v1/order/store/add", description="상점 추가",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["store"]
    )
async def addStore(store: Store, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            store_code = generate_random_string(24)
            new_store = StoreTable(
                store_code=store_code,
                store_name=store.store_name,
                store_status=store.store_status
            )
            if StocksCommands().create(session, new_store) == None:
                return JSONResponse(status_code=200, content={"message": "success", "store_code": store_code})
            else:
                return JSONResponse(status_code=400, content={"message": "fail"})
            
    except Exception as e:
        return {"message": str(e)}
@app.get(
        "/api/v1/order/store/list", description="상점 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["store"]
    )
async def stores(_: Annotated[User, Depends(getCurrentUser)], store_code: Union[str, None] = None, store_status: Union[bool, None] = None):
    try:
        with sessionFix() as session:
            storeData = StocksCommands().readStore(session, StoreTable, store_code=store_code, store_status=store_status)
            storeDataList = []
            for i in storeData:
                storeDataList.append({
                    "store_code": i.store_code,
                    "store_name": i.store_name,
                    "store_status": i.store_status
                })
            return JSONResponse(status_code=200, content={"message": "success", "stores": storeDataList})
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})
    
@app.get(
        "/api/v1/order/store/users/list", description="상점 유저 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["store"]
    )
async def storeUsers(temp: Annotated[User, Depends(getCurrentUser)], store_code: str, user_id: Union[str, None] = None):
    try:
        with sessionFix() as session:
            storeUsersData = StocksCommands().readStoreUsers(session, StoreTable, store_code=store_code, user_id=user_id)
            storeUserDataList = []
            for i in storeUsersData:
                storeUserDataList.append({
                    "store_code": i.store_code,
                    "user_id": i.user_id,
                    "user_type": i.user_type
                })
            return JSONResponse(status_code=200, content={"message": "success", "storeUsers": storeUserDataList})
    except Exception as e:
        return {"message": str(e)}

# 상점 정보 변경
@app.put(
        "/api/v1/order/store/update", description="상점 정보 변경",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["store"]
    )
async def updateStore(store: Store, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            target = StoreTable(
                store_code=store.store_code,
                store_name=store.store_name,
                store_status=store.store_status
            )
            if StocksCommands().updateStoreInfo(session, StoreTable, target) == None:
                return {"message": "success"}
            else:
                return HTTPException(status_code=400, detail="fail")
            
    except Exception:
        return {"message": "로그인이 필요합니다."}
    

# 상점 유저 정보 변경
@app.put(
        "/api/v1/order/store/users/update", description="상점 유저 정보 변경",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["store"]
    )
async def updateStoreUser(storeUser: StoreUser, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            target = StoreUserTable(
                store_code=storeUser.store_code,
                user_id=storeUser.user_id,
                user_type=storeUser.user_type
            )
            if StocksCommands().updateStoreUserInfo(session, StoreUserTable, target) == None:
                return {"message": "success"}
            else:
                return HTTPException(status_code=400, detail="fail")
            
    except Exception:
        return {"message": "로그인이 필요합니다."}