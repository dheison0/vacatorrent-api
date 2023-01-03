from bs4 import BeautifulSoup

from ... import SITE_URL
from ...utils import fetch
from ..errors import PageNotFound
from ..responses import SearchResult


async def getResults(query: str, page: int = 1) -> list[SearchResult]:
    responseText, _ = await fetch(f"{SITE_URL}/torrent-{query}/{page}")
    root = BeautifulSoup(responseText, 'lxml')
    rawResults = root.findAll('div', class_='row semelhantes')
    if not rawResults:
        raise PageNotFound(f'Page {page} of search "{query}" not found')
    results = list(map(
        lambda item: SearchResultExtractor(item).extract(),
        rawResults
    ))
    return results


class SearchResultExtractor:
    def __init__(self, root: BeautifulSoup):
        self._root = root

    def extract(self) -> SearchResult:
        return SearchResult(
            title=self.title(),
            sinopse=self.sinopse(),
            thumbnail=self.thumbnail(),
            url=self.url(),
            path=self.path()
        )

    def title(self) -> str:
        title = self._root.find('h2').text.lower()
        # Remove item type
        title = title.split(
            'série')[-1].split('filme')[-1].split('desenho')[-1]
        # Remove suffix
        title = title.split('torrent')[0].split('download')[0]
        return title.strip().capitalize()

    def sinopse(self) -> str:
        rawSinopse = self._root.find('p', class_='text-justify')
        sinopse: str = rawSinopse.text
        sinopseTitle: str = rawSinopse.next.text
        # Remove item title
        sinopse = sinopse.replace(sinopseTitle, '')
        # Remove download suffix of sinopse
        sinopse = sinopse.split('. Baixar')[0]+'.'
        return sinopse.strip()

    def thumbnail(self) -> str:
        img = self._root.find('img', class_='capa_imagem img-responsive')
        thumbnail: str = img.get('src')
        return thumbnail

    def url(self) -> str:
        url: str = self._root.find('a').get('href')
        return url

    def path(self) -> str:
        url = self.url()
        path = url.split('vacatorrent.com/')[-1]
        return path
