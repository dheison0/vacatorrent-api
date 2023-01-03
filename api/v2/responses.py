from dataclasses import dataclass


@dataclass
class Recommendation:
    title: str
    genre: str
    thumbnail: str
    year: int
    rating: float
    url: str
    path: str


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


@dataclass
class SearchResult:
    title: str
    sinopse: str
    thumbnail: str
    path: str


@dataclass
class Response:
    result: Download | list[Recommendation] | list[SearchResult]
    ok: bool = True


@dataclass
class Error:
    message: str
    ok: bool = False
