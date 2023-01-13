from bs4 import BeautifulSoup, Tag

from ... import SITE_URL
from ...utils import fetch
from ..errors import PageNotFound
from ..responses import Recommendation


async def getPage(pageNumber: int = 1) -> tuple[Recommendation]:
    response, _ = await fetch(f"{SITE_URL}/-{pageNumber}")
    root = BeautifulSoup(response, 'lxml')
    if root.find('a', href='torrent-indefinida-404'):
        raise PageNotFound(f"Webpage {pageNumber} not found!")
    recommendations = root.findAll('li', class_='capa_lista text-center')
    result = tuple(map(
        lambda item: RecommendationExtractor(item).extract(),
        recommendations
    ))
    return result


class RecommendationExtractor:
    def __init__(self, container: Tag):
        self._root = container
        self._hidden = container.find('div', class_='info_list')
        self._informations = container.find('p').text.split()

    def extract(self) -> Recommendation:
        return Recommendation(
            title=self.title(),
            genre=self.genre(),
            language=self.language(),
            year=self.year(),
            rating=self.rating(),
            thumbnail=self.thumbnail(),
            path=self.path()
        )

    def title(self) -> str:
        tag = self._root.find('h2')
        title = tag.text.replace('Torrent', '')
        return title.strip()

    def genre(self) -> str:
        genre = self._informations[0]
        return genre

    def thumbnail(self) -> str:
        tag = self._root.find('img')
        source: str = tag.get('src')
        return source

    def year(self) -> int:
        year = next(filter(
            lambda i: i if i.isdecimal() else None,
            self._informations
        ))
        return int(year)

    def rating(self) -> float:
        tag = self._root.find('div', class_='imdb_lista')
        rating = tag.text.strip().replace(',', '.')
        return float(rating)

    def path(self) -> str:
        url: str = self._root.find('a').get('href')
        path = url.split('vacatorrent.com/')[-1]
        return path

    def language(self) -> str:
        language = self._root.find('div', class_='idioma_lista').text
        return language.strip()
