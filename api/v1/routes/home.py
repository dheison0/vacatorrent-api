from http import HTTPStatus
from logging import error, info
from sanic import json
from ..extractors import home as home_extractor
from ...utils import log_exception

async def handler(_, page: int = 1):
    "Obtem todos os filmes/series recomendados pelo site"
    try:
        recommendations = await home_extractor.get_all(page)
    except Exception as exc:
        error("Home: params: page=%s", page)
        log_exception(exc)
        return json(
            body={'error': f'failed to get homepage recommendations: {str(exc)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    result = json(
        body=list(map(lambda r: r.dict(), recommendations)),
        status=HTTPStatus.OK
    )
    return result
