from .search import getResults
from ..responses import SearchResult
from ..errors import PageNotFound
import pytest


@pytest.mark.asyncio
async def test_getResults():
    resultPageOne = await getResults('alice', 1)
    assert isinstance(resultPageOne, list)
    assert len(resultPageOne) > 0
    assert isinstance(resultPageOne[0], SearchResult)
    resultPageTwo = await getResults('alice', 2)
    assert resultPageOne != resultPageTwo


@pytest.mark.asyncio
async def test_getResultsIndexOutOfBound():
    with pytest.raises(PageNotFound):
        await getResults('alice', 50)
