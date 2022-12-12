from dataclasses import asdict
from aiohttp import ClientSession
import logging, traceback

class Dataclass2Dict:
    def dict(self) -> dict[str, any]:
        return asdict(self)


async def http_get(url: str, *args, **kwargs) -> tuple[str, int]:
    async with ClientSession() as session:
        async with session.get(url, *args, **kwargs) as response:
            text = await response.text()
            code = response.status
            return text, code


def log_exception(e: Exception):
    stack = traceback.format_exception(e)
    stack_text = ''.join(stack)
    logging.error(stack_text)
