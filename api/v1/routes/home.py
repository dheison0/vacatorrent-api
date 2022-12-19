from http import HTTPStatus

from sanic import json

from ...caching import cache_response
from ...utils import log_exception
from ..extractors import home as home_extractor


@cache_response(60)
async def handler(_, page: int = 1):
    "Obtem todos os filmes/series recomendados pelo site"
    try:
        recommendations = await home_extractor.get_all(page)
    except Exception as err:
        log_exception(err)
        return json(
            body={'error': f'failed to get homepage recommendations: {str(err)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    result = json(
        body=list(map(lambda r: r.dict(), recommendations)),
        status=HTTPStatus.OK
    )
    return result
