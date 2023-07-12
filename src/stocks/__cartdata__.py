from fastapi.responses import JSONResponse, Response

from src.database.__conn__ import conn
from src.database.__cart__ import Cart
from src.settings.dependency import *

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
    product_id: str,
    product_price: str,
    product_count: str,
    session: SessionCookie = Depends(cookie),
):
    if session:
        user_id = session.user_id
        cart = Cart(user_id=user_id, product_id=product_id,
                    product_price=product_price, product_count=product_count)
        conn.add(cart)
        conn.rdsSession().commit()
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
async def cartList(session: SessionCookie = Depends(cookie)):
    if session:
        user_id = session.user_id
        cart = conn.rdsSession().query(Cart).filter_by(user_id=user_id).all()
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
async def cartList(session: SessionCookie = Depends(cookie)):
    if session:
        user_id = session.user_id
        cart = conn.rdsSession().query(Cart).filter_by(user_id=user_id).all()

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
    session: SessionCookie = Depends(cookie),
):
    if session:
        user_id = session.user_id
        cart = conn.rdsSession().query(Cart).filter_by(
            user_id=user_id, product_id=product_id).first()
        conn.rdsSession().delete(cart)
        conn.rdsSession().commit()
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
    session: SessionCookie = Depends(cookie),
):
    if session:
        user_id = session.user_id
        cart = conn.rdsSession().query(Cart).filter_by(
            user_id=user_id, product_id=product_id).first()
        
        # cart.product_count를 int로 변경
        tmpCount = int(cart.product_count)
        tmpCount += product_count
        cart.product_count = str(tmpCount)
        conn.rdsSession().commit()
        return {"message": "장바구니에서 수정되었습니다."}
    else:
        return {"message": "로그인이 필요합니다."}