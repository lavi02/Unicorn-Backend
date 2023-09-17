from fastapi import  Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject

from src.database.stores.store import StoreTable, Store
from src.database.users.user import UserTable
from src.services.crud.stores.store import StoreCommands
from src.services.crud.users.user import UserCommands

from src.services.util.hash import (
    getCurrentUser, generate_random_string, UserToken
)
from src.services.__init__ import app
from src.database.__init__ import get_db

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
            return JSONResponse(status_code=200, content={"message": "success", "store_code": store_code})
        else:
            return JSONResponse(status_code=400, content={"message": "fail"})

    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})