from fastapi.responses import JSONResponse

from src.database.__order__ import Order, OrderTable
from src.stocks.__crud_order__ import OrderCommands
from src.settings.dependency import *

from src.Users.__users__ import *
from src.Users.hash import *

from src.settings.dependency import app, sessionFix


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
    status_code=status.HTTP_200_OK, response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"},
        401: {"description": "권한 없음"}
    }, tags=["order"]
)
async def addOrder(order: Order, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            new_order = OrderTable(
                user_id=temp.username,
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
                return {"message": "fail"}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

# 장바구니 목록


@app.get(
    "/api/v1/order/list/all", description="전체 사용자의 주문 목록 조회",
    status_code=status.HTTP_200_OK, response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"},
        401: {"description": "로그인이 필요합니다."}
    }, tags=["order"]
)
async def orderListAll(_: Annotated[User, Depends(getCurrentUser)], store_code: str = None, table_number: str = None, status: bool = False):
    try:
        with sessionFix() as session:
            order = OrderCommands().read(session, OrderTable)
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
    except:
        return JSONResponse(status_code=400, content={"message": "fail"})

# 특정 사용자의 장바구니 목록
# 세션 활용


@app.get(
    "/api/v1/order/list", description="장바구니 특정 사용자 목록",
    status_code=status.HTTP_200_OK, response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"}
    }, tags=["order"]
)
async def orderList(temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            order = OrderCommands().read(session, OrderTable, id=temp.username)
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
    except Exception:
        return JSONResponse(status_code=400, content={"message": "fail"})


@app.delete(
    "/api/v1/order/delete",
    description="주문 취소",
    status_code=status.HTTP_200_OK, response_class=JSONResponse,
    responses={
        200: {"description": "성공"},
        400: {"description": "실패"},
        401: {"description": "로그인이 필요합니다."}
    }, tags=["order"]
)
async def deleteCart(
    product_id: str,
    temp: Annotated[User, Depends(getCurrentUser)]
):
    try:
        with sessionFix() as session:
            OrderCommands().delete(session, OrderTable,
                                   user_id=temp.username, product_id=product_id)
            return JSONResponse(status_code=200, content={"message": "success"})
    except Exception:
        return JSONResponse(status_code=400, content={"message": "fail"})
