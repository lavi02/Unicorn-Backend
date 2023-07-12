from fastapi.responses import RedirectResponse

from src.database.__conn__ import *
from src.database.__user__ import *

from src.Users.__users__ import *
from src.stocks.__cartdata__ import *
from src.settings.dependency import app

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")