from fastapi import Depends

from src.database.__conn__ import *
from src.settings.dependency import *
from src.Users.__users__ import *


# 현재 세션에 해당 사용자가 있는지 확인하는 함수
async def check_session(session: UUID = Depends(cookie)):
    tmpSession = await backend.read(session)
    if tmpSession == None:
        return False
    
    # redis에도 있는지 확인
    if not redisSession.getData(str(session)):
        return False
    
    return tmpSession