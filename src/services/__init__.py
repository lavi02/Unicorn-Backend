from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.database.__setup__ import check_and_create_table
tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
    },
    {
        "name": "product",
        "description": "Operations with products",
    },
    {
        "name": "order",
        "description": "Operations with orders",
    },
    {
        "name": "cart",
        "description": "Operations with cart",
    },
    {
        "name": "store",
        "description": "Operations with store",
    }
]

app = FastAPI(
    title="Document for Unicorn API",
    version="1.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# check_and_create_table()
