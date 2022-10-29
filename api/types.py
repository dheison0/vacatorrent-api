from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from .util import Dataclass2Dict

@dataclass_validate
@dataclass
class Link:
    title: str
    url: str


@dataclass_validate
@dataclass
class Download(Dataclass2Dict):
    title: str
    sinopse: str
    thumbnail: str
    year: int
    rating: float
    links: list[Link]


@dataclass_validate
@dataclass
class HomeResult(Dataclass2Dict):
    title: str
    imdb: float
    year: int
    talk_type: str
    thumbnail: str
    url: str


@dataclass_validate
@dataclass
class SearchResult(Dataclass2Dict):
    title: str
    description: str
    thumbnail: str
    url: str
