

from src.database.__conn__ import *
from src.database.__user__ import *
from src.Users.__users__ import *
from src.settings.dependency import app



@app.get("/")
async def root():
    return {"message": "Hello World"}