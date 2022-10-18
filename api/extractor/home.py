from bs4 import BeautifulSoup
from ..types import search
import requests

def getAll() -> list[search.SearchResult]:
    home = requests.get('https://vacatorrent.com/').text
    html = BeautifulSoup(home, 'html.parser')
    raw_results = html.findAll('li', class_='capa_lista text-center')
    search_results = []
    for raw_result in raw_results:
        year = raw_result.find('p').text.split('\r\n\t\t\t\t\t\t')
        result = search.SearchResult(
            title=raw_result.find('h2').text,
            imdb=float(raw_result.find('div', class_='imdb_lista').text),
            year=int(year[1]),
            talk_type=raw_result.find('div', class_='idioma_lista').text.strip(),
            thumbnail=raw_result.find('img').get('src'),
            url=raw_result.find('a').get('href')
        )
        search_results.append(result)
    return search_results
