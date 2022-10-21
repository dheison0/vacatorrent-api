from dataclasses import dataclass
from ..util.datahelper import Dataclass2Dict


@dataclass
class Link:
    title: str
    url: str


@dataclass
class Download(Dataclass2Dict):
    title: str
    sinopse: str
    thumbnail: str
    year: int
    rating: float
    links: list[Link]
