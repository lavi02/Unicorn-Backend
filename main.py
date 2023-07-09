from fastapi import FastAPI

from .src.database.__conn__ import conn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
