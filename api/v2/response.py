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


@dataclass
class Link:
    title: str
    url: str


@dataclass
class Download:
    title: str
    sinopse: str
    rating: float | None
    thumbnail: str
    links: list[Link]