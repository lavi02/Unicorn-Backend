from fastapi import Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject
from typing import Union

from src.database.stores.store import StoreTable, Store, reqStoreData
from src.database.stores.tables.table import StoreTableData
from src.database.users.user import UserTable

from src.services.crud.stores.store import StoreCommands
# from src.services.crud.stores.generated import GeneratedCommands
from src.services.crud.stores.table import TableCommands
# from src.services.crud.stores.user import StoreUserCommands
# from src.services.crud.stores.log import StoreLogCommands
from src.services.crud.users.user import UserCommands

from src.services.util.hash import (
    getCurrentUser, generate_random_string, UserToken
)
from src.services.__init__ import app
from src.database.__init__ import get_db


@app.get(
    "/api/v1/store/list", description="상점 정보 가져오기",
    tags=["store"], name="상점 정보 가져오기",
)
@inject
async def getStore(store_code: str = None, session=Depends(get_db)):
    try:
        store = StoreCommands().read(session=session, where=StoreTable, store_code=store_code)
        if store == None:
            return JSONResponse(status_code=400, content={"message": "fail"})
        else:
            storeList = []
            for i in store:
                storeList.append({
                    "store_code": i.store_code,
                    "store_name": i.store_name,
                    "store_status": i.store_status
                })

            return JSONResponse(status_code=200, content={"message": "success", "store": storeList})
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})


@app.post(
    "/api/v1/store/add", description="상점 추가",
    tags=["store"], name="상점 추가",
)
@inject
async def addStore(store: Store, token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        user = UserCommands().read(session=session, where=UserTable, id=token.username)
        if user.user_type == 0:
            return JSONResponse(status_code=400, content={"message": "Unauthorized"})
        store_code = generate_random_string(24)
        new_store = StoreTable(
            store_code=store_code,
            store_name=store.store_name
        )

        if StoreCommands().create(session, new_store) == None:
            newTables = []
            for i in range(store.table_count):
                newTables.append(StoreTableData(
                    store_code=store_code,
                    table_number=i+1
                ))
            print(newTables)

            if TableCommands().createMultiple(session, newTables) == None:
                return JSONResponse(status_code=200, content={"message": "success", "store_code": store_code})
            else:
                return JSONResponse(status_code=400, content={"message": "fail"})
        else:
            return JSONResponse(status_code=400, content={"message": "fail"})

    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})


@app.put(
    "/api/v1/store/update", description="상점 정보 수정",
    tags=["store"], name="상점 정보 수정",
)
@inject
async def updateStore(store: reqStoreData, token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        user = UserCommands().read(session=session, where=UserTable, id=token.username)
        if user.user_type == 0:
            return JSONResponse(status_code=400, content={"message": "Unauthorized"})

        new_store = reqStoreData(
            store_code=store.store_code,
            store_name=store.store_name,
            store_status=store.store_status
        )
        if StoreCommands().update(session, where=StoreTable, target=new_store) == None:
            return JSONResponse(status_code=200, content={"message": "success"})
        else:
            return JSONResponse(status_code=400, content={"message": "fail"})
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})


@app.delete(
    "/api/v1/store/delete", description="상점 삭제",
    tags=["store"], name="상점 삭제",
)
@inject
async def deleteStore(store_code: str, token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        user = UserCommands().read(session=session, where=UserTable, id=token.username)
        if user.user_type == 0:
            return JSONResponse(status_code=400, content={"message": "Unauthorized"})
        if StoreCommands().delete(session, where=StoreTable, store_code=store_code) == None:
            return JSONResponse(status_code=200, content={"message": "success"})
        else:
            return JSONResponse(status_code=400, content={"message": "fail"})
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})
