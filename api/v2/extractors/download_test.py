import pytest

from ..errors import PageNotFound
from ..responses import Download
from .download import getDownload


@pytest.mark.asyncio
async def test_download():
    result = await getDownload('9-1-1-6-temporada-legendada-torrent')
    assert isinstance(result, Download)
    if isinstance(result.rating, float):
        assert result.rating > 0
    assert len(result.links) > 0


@pytest.mark.asyncio
async def test_downloadNotFound():
    with pytest.raises(PageNotFound):
        await getDownload('khsfdhdiakdf')
