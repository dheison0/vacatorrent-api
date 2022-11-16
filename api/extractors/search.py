from bs4 import BeautifulSoup
from bs4.element import Tag
from .. import SITE
from ..utils import http_get
from ..types import SearchResult


async def search(query: str, page: int = 1) -> tuple[list[SearchResult] | None, bool | str]:
    raw, _ = await http_get(f'{SITE}/torrent-{query}/{page}', timeout=15)
    root = BeautifulSoup(raw, 'lxml')
    containers = root.findAll('div', class_='row semelhantes')
    query_results = []
    for container in containers:
        result = await get_result(container)
        query_results.append(result)
    pagination = root.find('ul', class_='pagination')
    if len(pagination) == 4:
        return None, "no results for this search"
    try:
        active_page = pagination.find('li', class_='active').find('a')
        last_page = pagination.findAll('li')[-1].find('a')
    except AttributeError:
        return None, f"page {page} of query '{query}' not found"
    has_next = active_page.get('href') != last_page.get('href')
    return (query_results, has_next), None


async def get_result(container: Tag):
    title = container.find('h2').text.split('FILME')[-1].split('ANIME')[-1]
    title = title.split('DESENHO')[-1].split('TORRENT')[0]
    description = container.find('p', class_='text-justify')
    return SearchResult(
        title=title.strip().title(),
        description=description.text.replace(description.next.text, '').strip(),
        thumbnail=container.find('img').get('src'),
        url=container.find('a').get('href').replace(SITE+'/', '')
    )
