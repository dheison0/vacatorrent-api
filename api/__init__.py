from os import getenv

from sanic import Sanic

SITE_URL = 'https://vacatorrent.com'
PORT = int(getenv("PORT", "5000"))

server = Sanic('VacaTorrent')
