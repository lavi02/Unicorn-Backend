from fastapi.responses import JSONResponse

from src.database.__conn__ import conn
from src.database.__cart__ import Cart, CartTable
from src.settings.dependency import *
from src.settings.check_session import check_session

from src.Users.__users__ import *
from src.Users.hash import *

from src.settings.dependency import app


# 장바구니 추가
@app.post(
        "/api/v1/cart/add", description="장바구니 품목 추가",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "권한 없음" }
        }, tags=["stocks"]
    )
async def addCart(
    cart: Cart,
    sessionUID: UUID = Depends(cookie),
):
    isSession = await check_session(sessionUID)
    if isSession:
        session = conn.rdsSession()
        user_id = isSession.user_id

        cart = CartTable(
            user_id=user_id,
            product_id=cart.product_id,
            product_price=cart.product_price,
            product_count=cart.product_count
        )
        session.add(cart)
        session.commit()
        session.close()
        return {"message": "장바구니에 추가되었습니다."}
    else:
        return {"message": "로그인이 필요합니다."}
    

# 장바구니 목록
@app.get(
        "/api/v1/cart/list/all", description="장바구니 전체 사용자 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["stocks"]
    )
async def cartList(sessionUID: UUID = Depends(cookie)):
    isSession = await check_session(sessionUID)
    if isSession:
        cart = conn.rdsSession().query(CartTable).all()
        conn.rdsSession().close()
        return cart
    else:
        return {"message": "로그인이 필요합니다."}
    

# 특정 사용자의 장바구니 목록
# 세션 활용
@app.get(
        "/api/v1/cart/list", description="특정 사용자의 장바구니 목록",
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
        user_id = isSession.user_id
        cart = conn.rdsSession().query(CartTable).filter_by(user_id=user_id).all()
        conn.rdsSession().close()

        # json response
        return cart
    else:
        return {"message": "로그인이 필요합니다."}

# 장바구니에서 해당 품목 삭제
@app.delete(
        "/api/v1/cart/delete",
        description="장바구니에서 해당 품목 삭제",
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
        user_id = isSession.user_id
        cart = conn.rdsSession().query(CartTable).filter_by(
            user_id=user_id, product_id=product_id).first()
        conn.rdsSession().delete(cart)
        conn.rdsSession().commit()
        conn.rdsSession().close()
        return {"message": "장바구니에서 삭제되었습니다."}
    else:
        return {"message": "로그인이 필요합니다."}
    

# 장바구니에서 상품 개수 수정
@app.put(
        "/api/v1/cart/update",
        description="장바구니에서 상품 개수 수정",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["stocks"]
    )
async def updateCart(
    product_id: str,
    product_count: int,
    sessionUID: UUID = Depends(cookie),
):
    isSession = await check_session(sessionUID)
    if isSession:
        user_id = isSession.user_id
        cart = conn.rdsSession().query(CartTable).filter_by(
            user_id=user_id, product_id=product_id).first()
        
        # cart.product_count를 int로 변경
        tmpCount = int(cart.product_count)
        tmpCount += product_count
        cart.product_count = str(tmpCount)
        conn.rdsSession().commit()
        conn.rdsSession().close()
        return {"message": "장바구니에서 수정되었습니다."}
    else:
        return {"message": "로그인이 필요합니다."}