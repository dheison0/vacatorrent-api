from dataclasses import dataclass
from functools import wraps
from threading import Thread
from time import sleep, time

from sanic import HTTPResponse, Request


@dataclass
class Cache:
    expiresAt: float
    response: HTTPResponse


storage: dict[str, Cache] = {}
stopCacheManager: bool = False
cacheManagerThread: Thread | None = None


def start():
    global cacheManagerThread
    cacheManagerThread = Thread(name="Cache Manager", target=cacheManager)
    cacheManagerThread.start()


def stop():
    global stopCacheManager
    if cacheManagerThread == None:
        return
    stopCacheManager = True
    cacheManagerThread.join()


def cacheManager():
    while not stopCacheManager:
        for url, cache in list(storage.items()):
            if cache.expiresAt < time():
                del storage[url]
        sleep(1)


def getCache(url: str) -> HTTPResponse | None:
    if url not in storage:
        return None
    return storage[url].response


def addCache(url: str, expiresIn: int, response: HTTPResponse):
    if response.status >= 300:
        return
    storage[url] = Cache(time()+expiresIn, response)


def cache(expires: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(req: Request, *args, **kwargs) -> HTTPResponse:
            cachedResponse = getCache(req.url)
            if cachedResponse:
                return cachedResponse
            response = await func(req, *args, **kwargs)
            addCache(req.url, expires, response)
            return response
        return wrapper
    return decorator
