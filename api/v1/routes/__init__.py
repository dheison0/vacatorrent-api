from sanic import Sanic
from sanic.blueprints import Blueprint

from . import download, home, search


def add_to_server(server: Sanic):
    v1 = Blueprint('v1', version=1)
    api = Blueprint.group(v1, version_prefix="/v")
    v1.add_route(home.handler, '/home', ["GET"])
    v1.add_route(home.handler, '/home/<page:int>', ["GET"])
    v1.add_route(search.handler, '/search', ["GET"])
    v1.add_route(download.handler, '/download/<key:str>', ["GET"])
    server.blueprint(api)
