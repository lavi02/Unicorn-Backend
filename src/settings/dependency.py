from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users",
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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)