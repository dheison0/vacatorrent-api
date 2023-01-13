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
    if cacheManagerThread is None:
        return
    stopCacheManager = True
    cacheManagerThread.join()


def cacheManager():
    while not stopCacheManager:
        for url in tuple(storage.keys()):
            if storage[url].expiresAt < time():
                del storage[url]
        sleep(1)


def getCache(url: str) -> HTTPResponse | None:
    cache = storage.get(url)
    return cache.response if cache else None


def addCache(url: str, expiresIn: int, response: HTTPResponse) -> None:
    if response.status < 300:
        storage[url] = Cache(time()+expiresIn, response)


def cache(expiresIn: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(req: Request, *args, **kwargs) -> HTTPResponse:
            cachedResponse = getCache(req.url)
            if cachedResponse:
                return cachedResponse
            response = await func(req, *args, **kwargs)
            addCache(req.url, expiresIn, response)
            return response
        return wrapper
    return decorator
