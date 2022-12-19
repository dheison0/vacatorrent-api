from dataclasses import dataclass
from random import randint

import pytest
from faker import Faker

from .utils import Dataclass2Dict, http_get


@dataclass
class Person(Dataclass2Dict):
    name: str
    age: int


fake = Faker()

def test_Dataclass2Dict():
    name = fake.name()
    age = randint(1, 100)
    result = Person(name, age).dict()
    expect = {'name': name, 'age': age}
    assert result == expect


@pytest.mark.asyncio
async def test_http_get():
    response, code = await http_get("https://httpbin.org/anything")
    assert isinstance(response, str)
    assert len(response) > 0
    assert code == 200
