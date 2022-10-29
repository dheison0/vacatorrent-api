from bs4 import BeautifulSoup
from requests import get
from ..types import HomeResult


def get_all() -> list[HomeResult]:
    home = get('https://vacatorrent.com/', timeout=5).text
    html = BeautifulSoup(home, 'lxml')
    raw_results = html.findAll('li', class_='capa_lista text-center')
    home_results = []
    for raw in raw_results:
        home_results.append(HomeResult(
            title=raw.find('h2').text,
            imdb=float(raw.find('div', class_='imdb_lista').text),
            year=int(raw.find('p').text.split('\r\n\t\t\t\t\t\t')[1]),
            talk_type=raw.find('div', class_='idioma_lista').text.strip(),
            thumbnail=raw.find('img').get('src'),
            url=raw.find('a').get('href')
        ))
    return home_results
