from . import extractors
from sanic import Sanic, Request, json
from sanic.blueprints import Blueprint
from http.server import HTTPStatus

def registry(server: Sanic):
    v1 = Blueprint('v1', version=1, )
    api = Blueprint.group(v1, version_prefix="/v")
    v1.add_route(home, '/', ["GET"])
    v1.add_route(home, '/<page:int>', ["GET"])
    v1.add_route(search, '/search', ["GET"])
    v1.add_route(download, '/download/<name:str>', ["GET"])
    server.blueprint(api)


async def home(_, page: int = 1):
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
        results, error = await extractors.search.search(query, page)
    except Exception as e:
        return json(
            body={'error': f'failed to search: {str(e)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    if error:
        return json({'error': error}, HTTPStatus.BAD_REQUEST)
    return json(
        body={
            'page': {'number': page, 'has_next': results[1]},
            'results': list(map(lambda r: r.dict(), results[0]))
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
