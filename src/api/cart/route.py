from fastapi import Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject
from typing import Union

from src.database.cart.cart import Cart, CartTable
from src.database.users.user import User, UserTable

from src.services.crud.cart.cart import CartCommands
from src.services.crud.users.user import UserCommands

from src.services.util.hash import (
    getCurrentUser, generate_random_string, UserToken
)
from src.services.__init__ import app
from src.database.__init__ import get_db


# 장바구니 추가
@app.post(
        "/api/v1/cart/add", description="장바구니 품목 추가",
        tags=["cart"], name="장바구니 품목 추가"
    )
@inject
async def addCart(cart: Cart, token: UserToken = Depends(getCurrentUser), session = Depends(get_db)):
    try:
        new_cart = CartTable(
            user_id=session.username,
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
        tags=["cart"], name="장바구니 전체 사용자 목록"
    )
@inject
async def cartListAll(session=Depends(get_db)):
    try:
        cart = CartCommands().read(session, where=CartTable)
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
        tags=["cart"], name="특정 사용자의 장바구니 목록"
    )
@inject
async def cartList(token: UserToken = Depends(getCurrentUser), session=Depends(get_db)):
    try:
        cart = CartCommands().read(session, CartTable, id=token.username)
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
        tags=["cart"]
    )
@inject
async def deleteCart(
    product_id: str,
    token: UserToken = Depends(getCurrentUser), session=Depends(get_db)
):
    try:
        CartCommands().delete(session, CartTable, user_id=token.username, product_id=product_id)
        return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

# 장바구니에서 상품 개수 수정
@app.put(
        "/api/v1/cart/update",
        description="장바구니에서 상품 개수 수정",
        tags=["cart"]
    )
@inject
async def updateCart(
    cart: Cart,
    token: UserToken = Depends(getCurrentUser), session=Depends(get_db)
):
    try:
        update_cart = CartCommands().read(session, CartTable, id=token.username, product_id=cart.product_id)
        update_cart.product_price = cart.product_price
        update_cart.product_count = cart.product_count

        CartCommands().update(session, update_cart)

        return JSONResponse(status_code=200, content={"message": "success"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": e})