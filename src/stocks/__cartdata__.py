from fastapi.responses import JSONResponse

from src.database.__conn__ import conn
from src.database.__cart__ import Cart, CartTable
from src.settings.dependency import *

from src.Users.__users__ import *
from src.Users.hash import *

from src.stocks.__crud__ import CartCommands
from src.settings.dependency import app, sessionFix


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
async def addCart(cart: Cart, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            new_cart = CartTable(
                user_id=temp.user_id,
                product_id=cart.product_id,
                product_price=cart.product_price,
                product_count=cart.product_count
            )
            if CartCommands().create(session, new_cart) == None:
                return {"message": "success"}
            else:
                return HTTPException(status_code=400, detail="fail")
            
    except Exception as e:
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
async def cartList(temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        try:
            with sessionFix() as session:
                cart = CartCommands().read(session, CartTable)
                return cart
        except:
            return HTTPException(status_code=400, detail="fail")
    except Exception as e:
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
async def cartList(sessionUID: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            cart = CartCommands().read(session, CartTable, id=sessionUID.user_id)
            return cart
    except:
        return HTTPException(status_code=400, detail="fail")

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
    temp: Annotated[User, Depends(getCurrentUser)],
):
    try:
        with sessionFix() as session:
            cart = CartCommands().delete(session, CartTable, user_id=temp.user_id, product_id=product_id)
            return {"message": "장바구니에서 삭제되었습니다."}
    except Exception as e:
        return HTTPException(status_code=400, detail=e)    

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
    cart: Cart,
    temp: Annotated[User, Depends(getCurrentUser)]
):
    try:
        with sessionFix() as session:
            update_cart = CartCommands().read(session, CartTable, id=temp.user_id, product_id=cart.product_id)
            print(update_cart)
            update_cart.product_count = cart.product_count

            CartCommands().update(session, CartTable, update_cart)
            return {"message": "장바구니에서 수정되었습니다."}
    except Exception as e:
        return HTTPException(status_code=400, detail=e)