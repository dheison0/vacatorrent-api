from dataclasses import dataclass
from ..util.datahelper import Dataclass2Dict


@dataclass
class SearchResult(Dataclass2Dict):
    title: str
    description: str
    thumbnail: str
    url: str
