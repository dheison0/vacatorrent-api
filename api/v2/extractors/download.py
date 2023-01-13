from bs4 import BeautifulSoup

from ... import SITE_URL
from ...utils import fetch
from ..errors import PageNotFound
from ..responses import Download, MagnetLink


async def getDownload(path: str) -> Download:
    response, _ = await fetch(f"{SITE_URL}/{path}")
    root = BeautifulSoup(response, 'lxml')
    if root.find('a', href='torrent-indefinida-404'):
        raise PageNotFound(f"Download webpage for path '{path}' not found!")
    download = DownloadExtractor(root).extract()
    return download


class DownloadExtractor:
    def __init__(self, root: BeautifulSoup):
        self._root = root

    def extract(self) -> Download:
        return Download(
            title=self.title(),
            sinopse=self.sinopse(),
            rating=self.rating(),
            thumbnail=self.thumbnail(),
            links=self.links()
        )

    def title(self) -> str:
        title = self._root.find('h1', class_='t_pagina').text.lower()
        title = title.split('torrent')[-1]  # Remove torrent prefix
        # Remove language type from end
        title = title.split('legendada')[0].split('download')[0]
        return title.strip().capitalize()

    def sinopse(self) -> str:
        container = self._root.find('div', class_='sinopse')
        tag = container.find('p')
        sinopse = tag.text.replace(tag.next.text, '').strip()
        return sinopse

    def rating(self) -> float | None:
        tag = self._root.find('a', itemprop='sameAs', rel='noopener')
        try:
            rating = tag.getText(strip=True).replace(',', '.')
        except:
            return None
        return float(rating)

    def thumbnail(self) -> str:
        tag = self._root.find('img', class_='img-responsive capa_imagem')
        thumbnail: str = tag.get('src')
        return thumbnail

    def links(self) -> tuple[MagnetLink]:
        rawLinks = self._root.findAll(
            name='a',
            class_='list-group-item list-group-item-success newdawn'
        )
        links = tuple(map(
            lambda item: MagnetLink(item.text.strip(), item.get('href')),
            rawLinks
        ))
        return links
