from . import extractors
from sanic import Sanic, Request, json
from http.server import HTTPStatus

def add_all(server: Sanic):
    server.add_route(lambda r: home(r, 1), '/', methods=["GET"])
    server.add_route(home, '/<page:int>', methods=["GET"])
    server.add_route(search, '/search', methods=["GET"])
    server.add_route(download, '/download/<name:str>', methods=["GET"])


async def home(_, page: int):
    "Obtem todos os filmes/series recomendados pelo site"
    try:
        recommendations = await extractors.home.get_all(page)
    except Exception as e:
        return json(
            body={'error': f'failed to get homepage recommendations: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return json(
        body=list(map(lambda r: r.dict(), recommendations)),
        status=HTTPStatus.OK
    )


async def search(request: Request):
    "Procura pelo filme desejado no site"
    query = request.args.get('q')
    if not query:
        return json(
            body={'error': 'query not specified'},
            status=HTTPStatus.BAD_REQUEST
        )
    page = int(request.args.get("page", "1"))
    try:
        search_results, has_next = await extractors.search.search(query, page)
    except Exception as e:
        return json(
            body={'error': f'failed to search: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return json(
        body={
            'page': {
                'number': page,
                'has_next': has_next
            },
            'results': list(map(lambda r: r.dict(), search_results))
        },
        status=HTTPStatus.OK
    )


async def download(_, name: str):
    "Obtem as informações de download de um filme/serie"
    try:
        result = await extractors.download.get_download(name)
    except Exception as e:
        return json(
            body={'error': f'failed to get download informations: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return json(body=result.dict(), status=HTTPStatus.OK)
