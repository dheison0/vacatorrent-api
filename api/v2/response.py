from dataclasses import dataclass


@dataclass
class Recommendation:
    title: str
    genre: str
    thumbnail: str
    year: int
    rating: float
    url: str
    id: str
