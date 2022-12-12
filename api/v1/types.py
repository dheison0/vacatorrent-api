from dataclasses import dataclass
from ..utils import Dataclass2Dict


@dataclass
class Link:
    title: str
    url: str


@dataclass
class Download(Dataclass2Dict):
    title: str
    sinopse: str
    thumbnail: str
    imdb: float
    links: list[Link]


@dataclass
class HomeResult(Dataclass2Dict):
    title: str
    imdb: float
    year: int | None
    talk_type: str
    thumbnail: str
    url: str


@dataclass
class SearchResult(Dataclass2Dict):
    title: str
    sinopse: str
    thumbnail: str
    url: str
