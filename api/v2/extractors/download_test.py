from dataclasses import asdict

import pytest

from ..errors import PageNotFound
from ..responses import Download, MagnetLink
from .download import getDownload


@pytest.mark.asyncio
async def test_download():
    result = await getDownload('9-1-1-6-temporada-legendada-torrent')
    assert isinstance(result, Download)
    for k, v in asdict(result).items():
        if k == 'rating':
            continue
        assert k and v
    assert isinstance(result.links, tuple)
    assert len(result.links) > 0
    for link in result.links:
        assert isinstance(link, MagnetLink)
        assert link.title != ""
        assert link.url != ""
    if isinstance(result.rating, float):
        assert result.rating > 0


@pytest.mark.asyncio
async def test_downloadNotFound():
    with pytest.raises(PageNotFound):
        await getDownload('khsfdhdiakdf')
