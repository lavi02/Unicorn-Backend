from fastapi import Request, HTTPException
from functools import wraps

from src.validation.query import *

def validate_empty_json_fields():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                json_body = await request.json()
                for key, value in json_body.items():
                    if value is None or value == "":
                        raise HTTPException(status_code=400, detail=f"{key} cannot be empty or null")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def validate_empty_query_params():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                query_params = request.query_params
                for key, value in query_params.items():
                    if value is None or value == "":
                        raise HTTPException(status_code=400, detail=f"{key} cannot be empty or null")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def validate_if_sqlquery_in_json():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                json_body = await request.json()
                for key, value in json_body.items():
                    for queryData in querys:
                        if queryData in value:
                            raise HTTPException(status_code=400, detail=f"{key} cannot be in json body")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def validate_if_sqlquery_in_query_params():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                query_params = request.query_params
                for key, value in query_params.items():
                    for queryData in querys:
                        if queryData in value:
                            raise HTTPException(status_code=400, detail=f"{key} cannot be in query params")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def isSpecialChr():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                json_body = await request.json()
                for key, value in json_body.items():
                    if value is not None:
                        for specialChr in specialStr:
                            if specialChr in value:
                                raise HTTPException(status_code=400, detail=f"{key} cannot be in json body")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
