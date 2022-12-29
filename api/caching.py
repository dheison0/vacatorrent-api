import gc
from dataclasses import dataclass
from functools import wraps
from threading import Thread
from time import sleep, time

from sanic import Request


@dataclass
class Cache:
    expire: float
    data: any


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
        async def wrapper(request: Request, *args, **kwargs):
            if request.url not in STORAGE:
                response = await func(request, *args, **kwargs)
                STORAGE[request.url] = Cache(time()+expire, response)
                if len(STORAGE) == 1:
                    Thread(target=cacheManager).start()
            return STORAGE[request.url].data
        return wrapper
    return decorator
