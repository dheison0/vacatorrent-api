from dataclasses import dataclass
from functools import wraps
from time import time

from sanic import HTTPResponse, Request


@dataclass
class Cache:
    expire: float
    data: HTTPResponse


def cacheResponse(expire: int = 60):
    def decorator(func):
        cache: dict[str, Cache] = {}
        @wraps(func)
        async def wrapper(req: Request, *args, **kwargs) -> HTTPResponse:
            if req.url in cache:
                if cache[req.url].expire > time():
                    return cache[req.url].data
                cache.pop(req.url)
            response: HTTPResponse = await func(req, *args, **kwargs)
            if response.status < 300:
                cache[req.url] = Cache(time()+expire, response)
            return response
        return wrapper
    return decorator
