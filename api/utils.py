from dataclasses import asdict
from aiohttp import ClientSession


class Dataclass2Dict:
    def dict(self) -> dict[str, any]:
        return asdict(self)


async def http_get(url: str, *args, **kwargs) -> tuple[str, int]:
    async with ClientSession() as session:
        async with session.get(url, *args, **kwargs) as response:
            text = await response.text()
            code = response.status
            return text, code
