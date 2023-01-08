from bs4 import BeautifulSoup

from ... import SITE_URL
from ...utils import fetch
from ..errors import NoResults, PageNotFound
from ..responses import SearchResult


async def getResults(query: str, page: int = 1) -> tuple[list[SearchResult], bool]:
    responseText, _ = await fetch(f"{SITE_URL}/torrent-{query}/{page}")
    root = BeautifulSoup(responseText, 'lxml')
    rawResults = root.findAll('div', class_='row semelhantes')
    if not rawResults and page == 1:
        raise NoResults(f"No results for query '{query}'")
    elif not rawResults:
        raise PageNotFound(f'Page {page} of search "{query}" not found')
    results = list(map(
        lambda item: SearchResultExtractor(item).extract(),
        rawResults
    ))
    pagination = root.find('ul', class_='pagination').findAll('li')
    hasNextPage = pagination[-2].get("class") is None
    return results, hasNextPage


class SearchResultExtractor:
    def __init__(self, root: BeautifulSoup):
        self._root = root

    def extract(self) -> SearchResult:
        return SearchResult(
            title=self.title(),
            sinopse=self.sinopse(),
            thumbnail=self.thumbnail(),
            path=self.path()
        )

    def title(self) -> str:
        tag = self._root.find('div', class_='col-sm-8 col-xs-12').find('h2')
        title = tag.text.lower()
        # Remove suffix
        title = title.split('torrent')[0].split('download')[0]
        # Remove prefix
        title = title.split('série')[-1].split('filme')[-1].split('desenho')[-1]
        return title.strip().capitalize()

    def sinopse(self) -> str:
        rawSinopse = self._root.find('p', class_='text-justify')
        sinopse: str = rawSinopse.text
        sinopseTitle: str = rawSinopse.next.text
        # Remove title from sinopse
        sinopse = sinopse.replace(sinopseTitle, '')
        # Remove download suffix of sinopse
        sinopse = sinopse.split('. Baixar')[0]+'.'
        return sinopse.strip()

    def thumbnail(self) -> str:
        img = self._root.find('img', class_='capa_imagem img-responsive')
        thumbnail: str = img.get('src')
        return thumbnail

    def path(self) -> str:
        url: str = self._root.find('a').get('href')
        path = url.split('vacatorrent.com/')[-1]
        return path
