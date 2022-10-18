from dataclasses import asdict
from json import dumps

class Dataclass2Dick:
    def dict(self) -> str:
        return asdict(self)

class Dataclass2JSON:
    def json(self) -> str:
        return dumps(self.dict())
