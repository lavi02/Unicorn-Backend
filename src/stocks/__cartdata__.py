from fastapi.responses import JSONResponse

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
        }, tags=["cart"]
    )
async def addCart(cart: Cart, temp: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            new_cart = CartTable(
                user_id=temp.username,
                table_number = cart.table_number,
                product_id=cart.product_id,
                product_price=cart.product_price,
                product_count=cart.product_count,
                product_option=cart.product_option
            )
            if CartCommands().create(session, new_cart) == None:
                return JSONResponse(status_code=200, content={"message": "success"})
            else:
                return JSONResponse(status_code=400, content={"message": "fail"})
            
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    

# 장바구니 목록
@app.get(
        "/api/v1/cart/list/all", description="장바구니 전체 사용자 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["cart"]
    )
async def cartLisAll(_: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            cart = CartCommands().read(session, CartTable)
            cartData = []
            for i in cart:
                cartData.append({
                    "user_id": i.user_id,
                    "table_number": i.table_number,
                    "product_id": i.product_id,
                    "product_price": i.product_price,
                    "product_count": i.product_count,
                    "product_option": i.product_option
                })

            return JSONResponse(status_code=200, content={"message": "success", "data": cartData})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    

# 특정 사용자의 장바구니 목록
# 세션 활용
@app.get(
        "/api/v1/cart/list", description="특정 사용자의 장바구니 목록",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["cart"]
    )
async def cartList(sessionUID: Annotated[User, Depends(getCurrentUser)]):
    try:
        with sessionFix() as session:
            cart = CartCommands().read(session, CartTable, id=sessionUID.username)
            cartList = []
            for i in cart:
                cartList.append({
                    "table_number": i.table_number,
                    "product_id": i.product_id,
                    "product_price": i.product_price,
                    "product_count": i.product_count,
                    "product_option": i.product_option
                })
            return JSONResponse(status_code=200, content={"message": "success", "data": cartList})
    except:
        return JSONResponse(status_code=400, content={"message": "fail"})

# 장바구니에서 해당 품목 삭제
@app.delete(
        "/api/v1/cart/delete",
        description="장바구니에서 해당 품목 삭제",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["cart"]
    )
async def deleteCart(
    product_id: str,
    temp: Annotated[User, Depends(getCurrentUser)],
):
    try:
        with sessionFix() as session:
            try:
                CartCommands().delete(session, CartTable, user_id=temp.username, product_id=product_id)
                return JSONResponse(status_code=200, content={"message": "success"})
            except:
                return JSONResponse(status_code=400, content={"message": "fail"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

# 장바구니에서 상품 개수 수정
@app.put(
        "/api/v1/cart/update",
        description="장바구니에서 상품 개수 수정",
        status_code=status.HTTP_200_OK, response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" },
            401: { "description": "로그인이 필요합니다." }
        }, tags=["cart"]
    )
async def updateCart(
    cart: Cart,
    temp: Annotated[User, Depends(getCurrentUser)]
):
    try:
        with sessionFix() as session:
            update_cart = CartCommands().read(session, CartTable, id=temp.username, product_id=cart.product_id)
            update_cart.product_price = cart.product_price
            update_cart.product_count = cart.product_count

            CartCommands().update(session, update_cart)

            return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": e})