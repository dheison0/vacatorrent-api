from dataclasses import dataclass
from ..util import datahelper

@dataclass
class SearchResult(datahelper.Dataclass2Dick):
    title: str
    imdb: float
    year: int
    talk_type: str
    thumbnail: str
    url: str
