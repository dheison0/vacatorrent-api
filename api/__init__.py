from os import getenv
from sanic import Sanic

SITE = 'https://vacatorrent.com'
PORT = int(getenv("PORT", "5000"))
DEBUG = getenv("DEBUG") is not None

server = Sanic(__name__)
