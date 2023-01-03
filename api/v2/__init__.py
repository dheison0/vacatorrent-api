from sanic import Sanic
from .handlers import home


def addRoutesToServer(server: Sanic):
    server.add_route(home.handler, '/v2/home/<page:int>')
