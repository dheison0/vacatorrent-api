from typing import Callable
from functools import wraps
from dataclasses import asdict
from sanic import json, HTTPResponse
from aiohttp import ClientSession


async def fetch(url: str, *args, **kwargs) -> tuple[str, int]:
    """
    Fetch data from url using GET method

    Returns response text and status code
    """
    session = ClientSession()
    response = await session.get(url, *args, **kwargs)
    text = await response.text()
    statusCode = response.status
    await session.close()
    return text, statusCode


def dataclassResponse(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> HTTPResponse:
        result, statusCode = await func(*args, **kwargs)
        resultDict = asdict(result)
        return json(resultDict, status=statusCode)
    return wrapper