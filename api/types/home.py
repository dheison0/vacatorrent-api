from dataclasses import dataclass
from ..util.datahelper import Dataclass2Dict

@dataclass
class HomeResult(Dataclass2Dict):
    title: str
    imdb: float
    year: int
    talk_type: str
    thumbnail: str
    url: str
