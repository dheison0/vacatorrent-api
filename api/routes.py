from . import extractors
from sanic import Sanic, Request, json


def add_all(server: Sanic):
    server.add_route(home, '/', methods=["GET"])
    server.add_route(search, '/search/<query>', methods=["GET"])
    server.add_route(download, '/download/<name>', methods=["GET"])


async def home(_):
    "Obtem todos os filmes/series recomendados pelo site"
    try:
        recommendations = await extractors.home.get_all()
    except Exception as error:
        result, code = {'error': f'failed to get homepage recommendations: {error}'}, 500
    else:
        result, code = {'results': list(map(lambda r: r.dict(), recommendations))}, 200
    return json(result, code)


async def search(request: Request, query: str):
    "Procura pelo filme desejado no site"
    page = int(request.args.get("page", "1"))
    try:
        search_results, has_next = await extractors.search.search(query, page)
    except Exception as error:
        result, code = {'error': f'failed to search: {error}'}, 500
    else:
        result = {
            'page': {
                'number': page,
                'has_next': has_next
            },
            'results': list(map(lambda r: r.dict(), search_results))
        }
        code = 200
    return json(result, code)


async def download(_, name: str):
    "Obtem as informações de download de um filme/serie"
    result = await extractors.download.get_download(name)
    return json(result.dict())