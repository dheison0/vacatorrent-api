from dataclasses import dataclass
from ..util import datahelper

@dataclass
class Movie(datahelper.Dataclass2JSON):
    title: str
    imdb: float
