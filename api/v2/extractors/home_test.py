from dataclasses import asdict

import pytest

from ..errors import PageNotFound
from ..responses import Recommendation
from .home import getPage


@pytest.mark.asyncio
async def test_getPage():
    pageOne = await getPage(1)
    assert isinstance(pageOne, tuple)
    assert len(pageOne) > 0
    for recommendation in pageOne:
        assert isinstance(recommendation, Recommendation)
        assert recommendation.year > 1800
        for k, v in asdict(recommendation).items():
            assert k and v
    pageTwo = await getPage(2)
    assert pageOne != pageTwo


@pytest.mark.asyncio
async def test_homepageExtractorInvalidPage():
    with pytest.raises(PageNotFound):
        await getPage(-12)
