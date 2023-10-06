from fastapi import Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject
from typing import Union

from src.database.orders.order import Order, OrderTable
from src.database.stores.store import StoreTable

from src.services.crud.order.order import OrderCommands
from src.services.crud.stocks.stocks import StocksCommands

from src.services.util.hash import (
    getCurrentUser, generate_random_string, UserToken
)
from src.services.__init__ import app
from src.database.__init__ import get_db


# user_id = Column(String(50), nullable=False)
# store_code = Column(String(50), nullable=False)
# table_number = Column(String(50), nullable=False)
# product_id = Column(String(50), primary_key=True, nullable=False)
# product_price = Column(String(50), nullable=False)
# product_count = Column(String(50), nullable=False)
# product_option = Column(JSON, nullable=True)
# product_status = Column(Boolean, nullable=False, default=False)
# 장바구니 추가
@app.post(
    "/api/v1/order/add", description="주문목록 추가",
    tags=["order"]
)
@inject
async def addOrder(order: Order, token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        new_order = OrderTable(
            user_id=token.username,
            store_code=order.store_code,
            table_number=order.table_number,
            product_id=order.product_id,
            product_price=order.product_price,
            product_count=order.product_count,
            product_option=order.product_option,
            product_status=order.product_status
        )
        if OrderCommands().create(session, new_order) == None:
            return {"message": "success"}
        else:
            return JSONResponse(status_code=400, content={"message": "fail"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

# 장바구니 목록
@app.get(
    "/api/v1/order/list/all", description="전체 사용자의 주문 목록 조회",
    tags=["order"]
)
@inject
async def orderListAll(token: UserToken = Depends(getCurrentUser), session=Depends(get_db), store_code: str = Union[str, None], status: bool = False):
    try:
        order = OrderCommands().read(session, OrderTable, store_cdoe=store_code, product_status=status)
        orderList = []
        for i in order:
            orderList.append({
                "user_id": i.user_id,
                "store_code": i.store_code,
                "table_number": i.table_number,
                "product_id": i.product_id,
                "product_price": i.product_price,
                "product_count": i.product_count,
                "product_option": i.product_option,
                "product_status": i.product_status
            })
        return JSONResponse(status_code=200, content={"message": "success", "data": orderList})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

# 특정 사용자의 장바구니 목록
# 세션 활용


@app.get(
    "/api/v1/order/list", description="장바구니 특정 사용자 목록",
    tags=["order"]
)
@inject
async def orderList(token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        order = OrderCommands().read(session, OrderTable, id=token.username)
        orderList = []
        for i in order:
            orderList.append({
                "user_id": i.user_id,
                "store_code": i.store_code,
                "table_number": i.table_number,
                "product_id": i.product_id,
                "product_price": i.product_price,
                "product_count": i.product_count,
                "product_option": i.product_option,
                "product_status": i.product_status
            })
        return JSONResponse(status_code=200, content={"message": "success", "data": orderList})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})


@app.delete(
    "/api/v1/order/delete",
    description="주문 취소",
    tags=["order"]
)
@inject
async def deleteCart(
    product_id: str,
    token: UserToken = Depends(getCurrentUser),
    session=Depends(get_db)
):
    try:
        OrderCommands().delete(session, OrderTable,
                                user_id=token.username, product_id=product_id)
        return JSONResponse(status_code=200, content={"message": "success"})
    except Exception:
        return JSONResponse(status_code=400, content={"message": "fail"})
    

@app.put(
    "/api/v1/order/status/update",
    description="주문 상태 변경", tags=["order"]
)
@inject
async def updateOrderStatus(
    store_code: str, product_id: str, product_status: bool,
    token: UserToken = Depends(getCurrentUser),
    session=Depends(get_db)
):
    try:
        totalPrice = 0
        orderData = OrderCommands().read(session, OrderTable, product_id=product_id, store_cdoe=store_code)
        for i in orderData:
            if not i.product_status:
                totalPrice += i.product_price * i.product_count
        OrderCommands().updateStatus(session, OrderTable,
                                user_id=token.username, product_id=product_id, status=product_status, store_code=store_code)
        StocksCommands().updateStoreTotalPrice(session, StoreTable, store_code=store_code, total_price=totalPrice)
        return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
