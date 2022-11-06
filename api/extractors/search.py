from bs4 import BeautifulSoup
from bs4.element import Tag
from .. import SITE
from ..utils import http_get
from ..types import SearchResult


async def search(query: str, page: int = 1) -> tuple[list[SearchResult], bool]:
    raw, _ = await http_get(f'{SITE}/torrent-{query}/{page}', timeout=5)
    root = BeautifulSoup(raw, 'lxml')
    containers = root.findAll('div', class_='row semelhantes')
    query_results = []
    for container in containers:
        result = await get_result(container)
        query_results.append(result)
    pagination = root.find('ul', class_='pagination').findAll('li')
    has_next = True
    if pagination[-2].get('class'):
        has_next = False
    return query_results, has_next


async def get_result(container: Tag):
    return SearchResult(
        title=container.find('h2').text,
        description=container.find('p', class_='text-justify').text,
        thumbnail=container.find('img').get('src'),
        url=container.find('a').get('href')
    )