from bs4 import BeautifulSoup
from bs4.element import Tag
from .. import SITE
from ..utils import http_get
from ..types import HomeResult


async def get_all() -> list[HomeResult]:
    raw, _ = await http_get(SITE, timeout=5)
    root = BeautifulSoup(raw, 'lxml')
    containers = root.findAll('li', class_='capa_lista text-center')
    home_results = []
    for container in containers:
        result = await get_recommendation(container)
        home_results.append(result)
    return home_results


async def get_recommendation(container: Tag) -> HomeResult:
    return HomeResult(
        title=container.find('h2').text,
        imdb=float(container.find('div', class_='imdb_lista').text),
        year=int(container.find('p').text.split('\r\n\t\t\t\t\t\t')[1]),
        talk_type=container.find('div', class_='idioma_lista').text.strip(),
        thumbnail=container.find('img').get('src'),
        url=container.find('a').get('href').replace(SITE+'/', '')
    )
