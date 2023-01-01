from bs4 import BeautifulSoup, Tag
from ..errors import PageNotFound
from ..response import Recommendation
from ...utils import httpGet
from ... import SITE_URL
import logging


async def homepageExtract(pageNumber: int = 1) -> list[Recommendation]:
    response, _ = await httpGet(f"{SITE_URL}/-{pageNumber}")
    root = BeautifulSoup(response, 'lxml')
    if root.find('a', href='torrent-indefinida-404'):
        raise PageNotFound(f"Webpage {pageNumber} not found!")
    recommendations = root.findAll('li', class_='capa_lista text-center')
    result = list(filter(
        lambda item: RecommendationExtractor(item).extract(),
        recommendations
    ))
    return result


class RecommendationExtractor:
    def __init__(self, container: Tag):
        self.__root = container

    def extract(self) -> Recommendation | None:
        try:
            result = Recommendation(
                title=self.title(),
                genre=self.genre(),
                thumbnail=self.thumbnail(),
                year=self.year(),
                rating=self.rating(),
                url=self.url(),
                id=self.id()
            )
        except Exception as exc:
            logging.exception(
                "Call to RecommendationExtractor.extract failed: %s", exc,
                stack_info=True
            )
            return None
        return result

    def title(self) -> str:
        tag = self.__root.find('h2')
        title = tag.text.replace('Torrent', '')
        return title.strip()

    def genre(self) -> str:
        tag = self.__root.find('div', class_='info_lista').find('p')
        informations = tag.text.split()
        genre = informations[0]
        return genre

    def thumbnail(self) -> str:
        tag = self.__root.find('img')
        source: str = tag.get('src')
        return source

    def year(self) -> int:
        tag = self.__root.find('div', class_='info_lista')
        informations = tag.text.split()
        year = next(filter(lambda i: i if i.isdecimal()
                    else None, informations))
        return int(year[-1])

    def rating(self) -> float:
        tag = self.__root.find('div', class_='imdb_lista')
        rating = tag.text.strip().replace(',', '.')
        return float(rating)

    def url(self) -> str:
        tag = self.__root.find('a')
        url: str = tag.get('href')
        return url

    def id(self) -> str:
        url = self.url()
        id = url.split('vacatorrent.com/')[-1]
        return id
