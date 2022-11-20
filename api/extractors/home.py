from bs4 import BeautifulSoup
from bs4.element import Tag
from .. import SITE
from ..utils import http_get
from ..types import HomeResult


async def get_all(page: int = 1) -> list[HomeResult]:
    raw, _ = await http_get(f'{SITE}/-{page}', timeout=15)
    root = BeautifulSoup(raw, 'lxml')
    containers = root.findAll('li', class_='capa_lista text-center')
    home_results = []
    for container in containers:
        result = await get_recommendation(container)
        home_results.append(result)
    return home_results


async def get_recommendation(container: Tag) -> HomeResult:
    title_tag = container.find('h2')
    title = title_tag.text.replace('Torrent', '').strip().capitalize()
    imdb_tag = container.find('div', class_='imdb_lista')
    imdb = (0.0 if not imdb_tag else imdb_tag.text.strip().replace(',', '.'))
    info = container.find('p').text.split()
    possible_year = list(filter(lambda i: i.isdecimal(), info))
    year = (None if not possible_year else int(possible_year[0]))
    talk_type = container.find('div', class_='idioma_lista').text.strip()
    thumbnail = container.find('img').get('src')
    url = container.find('a').get('href').replace(SITE+'/', '')
    return HomeResult(title, float(imdb), year, talk_type, thumbnail, url)
