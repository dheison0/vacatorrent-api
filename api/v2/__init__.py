from sanic import Sanic

from .handlers import home, download, search


def addRoutesToServer(server: Sanic):
    server.add_route(home.handler, '/v2/home/<page:int>')
    server.add_route(download.handler, '/v2/download/<path:str>')
    server.add_route(search.handler, '/v2/search')
