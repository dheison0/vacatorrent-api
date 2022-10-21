from bs4 import BeautifulSoup
from requests import get
from ..types.download import Download, Link


def get_download(location: str) -> Download:
    page = get(f'https://vacatorrent.com/{location}', timeout=5).text
    html = BeautifulSoup(page, 'html.parser')
    infos = html.find('div', class_='infos')
    sinopse = html.find('p', class_='text-justify')
    links = []
    for tag in html.findAll('a', class_="list-group-item list-group-item-success newdawn"):
        links.append(Link(
            title=tag.get('title'),
            url=tag.get('href')
        ))
    return Download(
        title=html.find('h1', class_='t_pagina').text.strip(),
        sinopse=sinopse.text.replace(sinopse.next.text, ''),
        thumbnail=html.find('img', class_='img-responsive capa_imagem').get('src'),
        year=int(infos.find('a').text),
        rating=float(infos.find('span', itemprop='ratingValue').text),
        links=links
    )
