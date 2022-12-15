from dataclasses import dataclass
from functools import wraps
from random import randint
from threading import Thread
from time import sleep, time
import gc


@dataclass
class Cache:
    expire: float
    data: any


STORAGE: dict[int, Cache] = {}
MANAGERS: int = 0


def cache_manager():
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


def cache_response(expire: int = 60):
    def decorator(func):
        cache_id = randint(1e10, 1e11-1)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if cache_id not in STORAGE:
                response = await func(*args, **kwargs)
                STORAGE[cache_id] = Cache(time()+expire, response)
                if len(STORAGE) == 1:
                    Thread(target=cache_manager).start()
            return STORAGE[cache_id].data
        return wrapper
    return decorator
