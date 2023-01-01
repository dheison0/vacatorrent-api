from bs4 import BeautifulSoup
from ..errors import PageNotFound
from ..response import Download, Link
from ... import SITE_URL
from ...utils import httpGet


async def getDownload(path: str) -> Download:
    response, statusCode = await httpGet(f"{SITE_URL}/{path}")
    if statusCode != 200:
        raise PageNotFound(f"Download webpage for path {path} not found!")
    root = BeautifulSoup(response, 'lxml')
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
        title = title.split('torrent')[-1].split('legendada')[0].split('download')[0]
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
    
    def links(self) -> list[Link]:
        rawLinks = self._root.findAll(
            name='a',
            class_='list-group-item list-group-item-success newdawn'
        )
        links = list(map(
            lambda item: Link(title=item.text.strip(), url=item.get('href')),
            rawLinks
        ))
        return links
