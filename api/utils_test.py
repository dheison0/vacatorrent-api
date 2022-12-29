from dataclasses import dataclass
from random import randint

import pytest
from faker import Faker

from .utils import Dataclass2Dict, httpGet


def test_Dataclass2Dict():
    @dataclass
    class Person(Dataclass2Dict):
        name: str
        age: int

    fake = Faker()
    name = fake.name()
    age = randint(1, 100)
    result = Person(name, age).dict()
    expect = {'name': name, 'age': age}
    assert result == expect


@pytest.mark.asyncio
async def test_httpGet():
    response, code = await httpGet("https://api.ipify.org?format=text")
    assert isinstance(response, str)
    assert response.count('.') == 3
    assert code == 200
