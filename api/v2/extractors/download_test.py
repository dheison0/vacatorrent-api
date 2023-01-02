from . import download
from ..errors import PageNotFound
import pytest


@pytest.mark.asyncio
async def test_download():
    result = await download.getDownload('9-1-1-6-temporada-legendada-torrent')
    if isinstance(result.rating, float):
        assert result.rating > 0
    assert len(result.links) > 0


@pytest.mark.asyncio
async def test_downloadNotFound():
    with pytest.raises(PageNotFound):
        await download.getDownload('khsfdhdiakdf')
