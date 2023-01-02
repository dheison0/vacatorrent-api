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
