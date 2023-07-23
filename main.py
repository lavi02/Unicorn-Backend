from fastapi.responses import RedirectResponse

from src.database.__conn__ import *
from src.database.__user__ import *
from src.database.__cart__ import *
from src.database.__order__ import *
from src.database.__store__ import *
from src.database.__stocks__ import *

from src.Users.__users__ import *
from src.stocks.__cartdata__ import *
from src.stocks.__orders__ import *
from src.stocks.store.__crud__ import *
from src.stocks.store.__store__ import *
from src.settings.dependency import app

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")