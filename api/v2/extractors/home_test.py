import pytest
from . import home


@pytest.mark.asyncio
async def test_homepageExtractor():
    resultOne = await home.homepageExtract(1)
    resultTwo = await home.homepageExtract(2)
    assert len(resultOne) > 0 and len(resultTwo) > 0
    assert resultOne != resultTwo


@pytest.mark.asyncio
async def test_homepageExtractorInvalidPage():
    with pytest.raises(home.PageNotFound):
        await home.homepageExtract(-12)
