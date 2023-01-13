from dataclasses import dataclass, field


@dataclass
class Recommendation:
    title: str
    genre: str
    language: str
    year: int
    rating: float
    thumbnail: str
    path: str


@dataclass
class MagnetLink:
    title: str
    url: str


@dataclass
class Download:
    title: str
    sinopse: str
    rating: float | None
    thumbnail: str
    links: tuple[MagnetLink]


@dataclass
class SearchResult:
    title: str
    sinopse: str
    thumbnail: str
    path: str


@dataclass
class Ok:
    result: Download | tuple[Recommendation] | tuple[SearchResult]
    ok: bool = field(default=True, init=False)


@dataclass
class Error:
    message: str
    ok: bool = field(default=False, init=False)
