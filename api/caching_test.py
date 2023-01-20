from dataclasses import dataclass
from random import random

import pytest

from . import caching


@dataclass
class RequestSPY:
    url: str

@dataclass
class HTTPResponseSPY:
    body: bytes
    status: int

def generateResponse() -> HTTPResponseSPY:
    return HTTPResponseSPY(
        body=f'hello {random()}'.encode('utf-8'),
        status=200
    )


@pytest.mark.asyncio
async def test_cache_with_custom_expiresIn():
    @caching.cache()
    async def mock_function(_: RequestSPY):
        return generateResponse()
    req = RequestSPY('/')
    result1 = await mock_function(req)
    result2 = await mock_function(req)
    assert result1 is result2


def test_cache_with_invalid_expiresIn():
    with pytest.raises(caching.InvalidCacheTime):
        caching.cache(-1)


@pytest.mark.asyncio
async def test_cache_with_invalid_response():
    @caching.cache()
    async def mock_function(_):
        return None
    await mock_function(RequestSPY('/buzz'))
    assert '/buzz' not in caching.storage


@pytest.mark.asyncio
async def test_cache_with_multiple_responses():
    @caching.cache()
    async def mock_function(_):
        return generateResponse()
    fooResponse = await mock_function(RequestSPY('/foo'))
    barResponse = await mock_function(RequestSPY('/bar'))
    fooCached = await mock_function(RequestSPY('/foo'))
    barCached = await mock_function(RequestSPY('/bar'))
    assert fooResponse is fooCached
    assert barResponse is barCached
