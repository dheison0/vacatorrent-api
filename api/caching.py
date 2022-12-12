from typing import Any
from time import sleep
from threading import Thread
from functools import wraps
import gc


def cache_response(timeout: int = 60) -> Any:
    def decorator(func):
        response: Any = None

        def clean():
            nonlocal response
            sleep(timeout)
            response = None
            gc.collect()

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal response
            if not response:
                response = await func(*args, **kwargs)
                Thread(target=clean).start()
            return response
        return wrapper
    return decorator
