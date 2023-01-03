from .home import getPage
from ..responses import Recommendation
from ..errors import PageNotFound
import pytest


@pytest.mark.asyncio
async def test_getPage():
    pageOne = await getPage(1)
    assert isinstance(pageOne, list)
    assert len(pageOne) > 0
    assert isinstance(pageOne[0], Recommendation)
    pageTwo = await getPage(2)
    assert pageOne != pageTwo


@pytest.mark.asyncio
async def test_homepageExtractorInvalidPage():
    with pytest.raises(PageNotFound):
        await getPage(-12)
