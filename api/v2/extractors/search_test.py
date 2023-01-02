from .search import getResults
from ..errors import PageNotFound
import pytest


@pytest.mark.asyncio
async def test_getResults():
    resultPageOne = await getResults('alice', 1)
    resultPageTwo = await getResults('alice', 2)
    assert len(resultPageOne) > 0
    assert len(resultPageTwo) > 0
    assert resultPageOne != resultPageTwo


@pytest.mark.asyncio
async def test_getResultsIndexOutOfBound():
    with pytest.raises(PageNotFound):
        await getResults('alice', 50)
