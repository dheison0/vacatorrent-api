import gc
from dataclasses import dataclass
from functools import wraps
from threading import Thread
from time import sleep, time
from typing import Any

from sanic import Request, HTTPResponse


@dataclass
class Cache:
    expire: float
    data: Any


STORAGE: dict[str, Cache] = {}
MANAGERS: int = 0

def cacheManager():
    """Manage cache storage"""
    global  MANAGERS
    MANAGERS += 1
    while len(STORAGE) > 0 and MANAGERS == 1:
        sleep(1)
        for cid, cache in list(STORAGE.items()):
            if time() >= cache.expire:
                STORAGE.pop(cid)
    MANAGERS -= 1
    gc.collect()


def cacheResponse(expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(req: Request, *args, **kwargs):
            if req.url not in STORAGE:
                response: HTTPResponse = await func(req, *args, **kwargs)
                if response.status >= 300:
                    return response
                STORAGE[req.url] = Cache(time()+expire, response)
                if len(STORAGE) == 1:
                    Thread(target=cacheManager).start()
            return STORAGE[req.url].data
        return wrapper
    return decorator
