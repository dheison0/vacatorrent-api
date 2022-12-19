import faker
import pytest

from . import extractors, types

fake = faker.Faker()


@pytest.mark.asyncio
async def test_home():
    def check_types(result: types.HomeResult):
        assert isinstance(result.title, str) and len(result.title) > 1
        assert isinstance(result.url, str) and len(result.url) > 1
        assert isinstance(result.thumbnail, str)
        assert isinstance(result.imdb, float) or result.imdb is None
        assert isinstance(result.talk_type, str)
    for i in range(1, 5):
        results = await extractors.home.get_all(i)
        any(map(check_types, results))


@pytest.mark.asyncio
async def test_search():
    def check_types(result: types.SearchResult):
        assert isinstance(result.title, str)
        assert isinstance(result.sinopse, str)
        assert isinstance(result.thumbnail, str)
        assert isinstance(result.url, str)
    query = 'Velozes e furiosos'
    has_next = True
    page = 1
    while has_next and page < 3:
        result, error = await extractors.search.search(query, page)
        if error:
            raise Exception(error)
        has_next = result[1]
        assert len(result[0]) > 0
        any(map(check_types, result[0]))
        page += 1


@pytest.mark.asyncio
async def test_download():
    results = [
        await extractors.download.get_download('velozes-e-furiosos-9-torrent'),
        await extractors.download.get_download('adao-negro-torrent')
    ]
    for result in results:
        assert isinstance(result.title, str)
        assert isinstance(result.sinopse, str)
        assert isinstance(result.thumbnail, str)
        assert isinstance(result.imdb, float)
        assert isinstance(result.links, list) and len(result.links) >= 1