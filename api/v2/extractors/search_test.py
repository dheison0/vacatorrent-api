from dataclasses import asdict

import pytest

from ..errors import PageNotFound
from ..responses import SearchResult
from .search import getResults


@pytest.mark.asyncio
async def test_getResults():
    resultPageOne, hasMore = await getResults('alice', 1)
    assert isinstance(resultPageOne, tuple)
    assert len(resultPageOne) > 0
    for result in resultPageOne:
        assert isinstance(result, SearchResult)
        for k, v in asdict(result).items():
            assert k and v
    assert hasMore is True
    resultPageTwo = await getResults('alice', 2)
    assert resultPageOne != resultPageTwo


@pytest.mark.asyncio
async def test_getResultsPageNotFound():
    with pytest.raises(PageNotFound):
        await getResults('alice', 50)
