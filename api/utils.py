from dataclasses import asdict
from functools import wraps
from typing import Callable

from aiohttp import ClientSession
from sanic import HTTPResponse, json


async def fetch(url: str, *args, **kwargs) -> tuple[str, int]:
    """
    Fetch data from url using GET method

    Returns response text and status code
    """
    session = ClientSession()
    response = await session.get(url, *args, **kwargs)
    text = await response.text()
    statusCode = response.status
    response.close()
    await session.close()
    return text, statusCode


def dataclassResponse(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> HTTPResponse:
        result, statusCode = await func(*args, **kwargs)
        resultDict = asdict(result)
        return json(resultDict, status=statusCode)
    return wrapper
