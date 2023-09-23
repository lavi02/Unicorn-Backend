from src.services.__init__ import app
from fastapi.responses import RedirectResponse
from src.services.util.logger import *

# router
from src.api.stores.route import *
from src.api.users.route import *


@app.get("/")
async def root():
    return RedirectResponse(url="https://ddingdong.pro")
