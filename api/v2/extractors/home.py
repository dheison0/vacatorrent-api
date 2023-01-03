from bs4 import BeautifulSoup, Tag

from ... import SITE_URL
from ...utils import fetch
from ..errors import PageNotFound
from ..responses import Recommendation


async def getPage(pageNumber: int = 1) -> list[Recommendation]:
    response, _ = await fetch(f"{SITE_URL}/-{pageNumber}")
    root = BeautifulSoup(response, 'lxml')
    if root.find('a', href='torrent-indefinida-404'):
        raise PageNotFound(f"Webpage {pageNumber} not found!")
    recommendations = root.findAll('li', class_='capa_lista text-center')
    result = list(map(
        lambda item: RecommendationExtractor(item).extract(),
        recommendations
    ))
    return result


class RecommendationExtractor:
    def __init__(self, container: Tag):
        self._root = container

    def extract(self) -> Recommendation:
        return Recommendation(
            title=self.title(),
            genre=self.genre(),
            thumbnail=self.thumbnail(),
            year=self.year(),
            rating=self.rating(),
            url=self.url(),
            path=self.path()
        )

    def title(self) -> str:
        tag = self._root.find('h2')
        title = tag.text.replace('Torrent', '')
        return title.strip()

    def genre(self) -> str:
        tag = self._root.find('div', class_='info_lista').find('p')
        informations = tag.text.split()
        genre = informations[0]
        return genre

    def thumbnail(self) -> str:
        tag = self._root.find('img')
        source: str = tag.get('src')
        return source

    def year(self) -> int:
        tag = self._root.find('div', class_='info_lista').find('p')
        informations = tag.text.split()
        year = next(filter(lambda i: i if i.isdecimal()
                    else None, informations))
        return int(year)

    def rating(self) -> float:
        tag = self._root.find('div', class_='imdb_lista')
        rating = tag.text.strip().replace(',', '.')
        return float(rating)

    def url(self) -> str:
        tag = self._root.find('a')
        url: str = tag.get('href')
        return url

    def path(self) -> str:
        url = self.url()
        path = url.split('vacatorrent.com/')[-1]
        return path
