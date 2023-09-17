from src.services.__init__ import app
from fastapi.responses import RedirectResponse

# router
from src.api.users.route import *

@app.get("/")
async def root():
    return RedirectResponse(url="https://ddingdong.pro")