from os import getenv
from sanic import Sanic

PORT = int(getenv("PORT", "5000"))

app = Sanic(__name__)
