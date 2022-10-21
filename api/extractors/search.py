from bs4 import BeautifulSoup
from requests import get
from ..types.search import SearchResult


def get_results(query: str, page: int = 1) -> tuple[list[SearchResult], bool]:
    page = get(f'https://vacatorrent.com/torrent-{query}/{page}', timeout=5).text
    html = BeautifulSoup(page, 'html.parser')
    raw_results = html.findAll('div', class_='row semelhantes')
    results = []
    for raw in raw_results:
        results.append(SearchResult(
            title=raw.find('h2').text,
            description=raw.find('p', class_='text-justify').text,
            thumbnail=raw.find('img').get('src'),
            url=raw.find('a').get('href')
        ))
    pagination = html.find('ul', class_='pagination').findAll('li')
    has_next = True
    if pagination[-2].get('class'):
        has_next = False
    return results, has_next
