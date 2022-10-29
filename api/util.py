from dataclasses import asdict

class Dataclass2Dict:
    def dict(self) -> str:
        return asdict(self)
