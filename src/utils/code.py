from src.stocks.store.__store__ import *
from src.stocks.store.__crud__ import *

@app.post(
        "/api/v1/utils/code/generate", description="상점 테이블별 코드 생성", response_class=JSONResponse,
        responses={
            200: { "description": "성공" },
            400: { "description": "실패" }
        }, tags=["utils"]
)
async def generateCode():
    try:
        with sessionFix() as session:
            result = StoreCommands().generateCode(session)
            return JSONResponse(status_code=200, content={"message": "success", "data": result})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})