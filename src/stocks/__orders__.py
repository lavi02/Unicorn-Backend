from fastapi.responses import JSONResponse

from src.database.__cart__ import Order, OrderTable
from src.stocks.__crud_order__ import OrderCommands
from src.settings.dependency import *
from src.settings.check_session import check_session

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
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["stocks"]
    )
async def addOrder(order: Order, sessionUID: UUID = Depends(cookie)):
    isSession = await check_session(sessionUID)
    if isSession:
        with sessionFix() as session:
            new_order = OrderTable(
                user_id=isSession.user_id,
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
                return HTTPException(status_code=400, detail="fail")
            
    else:
        return {"message": "로그인이 필요합니다."}
    

# 장바구니 목록
@app.get(
        "/api/v1/order/list/all", description="장바구니 전체 사용자 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["stocks"]
    )
async def orderList(sessionUID: UUID = Depends(cookie), store_code: str = None, table_number: str = None, status: bool = None):
    isSession = await check_session(sessionUID)
    if isSession:
        try:
            with sessionFix() as session:
                cart = OrderCommands().readTableOrder(session, OrderTable, store_code=store_code, table_number=table_number, status=status)
                return cart
        except:
            return HTTPException(status_code=400, detail="fail")
    else:
        return {"message": "로그인이 필요합니다."}
    

# 특정 사용자의 장바구니 목록
# 세션 활용
@app.get(
        "/api/v1/order/list", description="특정 사용자의 주문 목록 조회",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["stocks"]
    )
async def cartList(sessionUID: UUID = Depends(cookie)):
    isSession = await check_session(sessionUID)
    if isSession:
        with sessionFix() as session:
            cart = OrderCommands().read(session, Order, id=isSession.user_id)
            return cart
    else:
        return {"message": "로그인이 필요합니다."}

# 장바구니에서 해당 품목 삭제
@app.delete(
        "/api/v1/order/delete",
        description="주문 취소",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["stocks"]
    )
async def deleteCart(
    product_id: str,
    sessionUID: UUID = Depends(cookie),
):
    isSession = await check_session(sessionUID)
    if isSession:
        with sessionFix() as session:
            OrderCommands().delete(session, OrderTable, user_id=isSession.user_id, product_id=product_id)
            return {"message": "장바구니에서 삭제되었습니다."}
    else:
        return {"message": "로그인이 필요합니다."}