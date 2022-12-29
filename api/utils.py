import logging
import traceback
from typing import Any
from dataclasses import asdict

from aiohttp import ClientSession


class Dataclass2Dict:
    """Add a function to convert a dataclass into dictionary"""

    def dict(self) -> dict[str, Any]:
        return asdict(self)


async def httpGet(url: str, *args, **kwargs) -> tuple[str, int]:
    """Send a request to a webserver and await for it's response"""
    session = ClientSession()
    response = await session.get(url, *args, **kwargs)
    responseText = await response.text()
    statusCode = response.status
    return responseText, statusCode


def logException(e: Exception):
    stackLines = traceback.format_exception(e)
    exceptionText = ''.join(stackLines)
    logging.error(exceptionText)
