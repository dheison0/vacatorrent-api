from . import download
import pytest


@pytest.mark.asyncio
async def test_download():
    result = await download.getDownload('9-1-1-6-temporada-legendada-torrent')
    assert result != None
    if isinstance(result.rating, float):
        assert result.rating > 0
    assert len(result.links) > 0