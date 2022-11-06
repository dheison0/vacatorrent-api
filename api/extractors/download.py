from bs4 import BeautifulSoup
from .. import SITE
from ..utils import http_get
from ..types import Download, Link


async def get_download(location: str) -> Download:
    raw, _ = await http_get(f'{SITE}/{location}', timeout=15)
    root = BeautifulSoup(raw, 'lxml')
    informations = root.find('div', class_='infos')
    sinopse = root.find('p', class_='text-justify')
    title = root.find('h1', class_='t_pagina').text
    title = title.split('TORRENT')[-1].split('DOWNLOAD')[0].strip()
    imdb = root.find('div', class_='col-sm-5').find('a', itemprop='sameAs')
    imdb = (0.0 if not imdb else float(imdb.text))
    return Download(
        title=title.title(),
        sinopse=sinopse.text.replace(sinopse.next.text, ''),
        thumbnail=root.find('img', class_='img-responsive capa_imagem').get('src'),
        imdb=imdb,
        links=extract_links(root)
    )


def extract_links(root: BeautifulSoup) -> list[Link]:
    links = []
    tag_attrs = {'class': 'list-group-item list-group-item-success newdawn'}
    for tag in root.findAll('a', tag_attrs):
        links += [Link(title=tag.get('title'), url=tag.get('href'))]
    return links