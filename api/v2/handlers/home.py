import logging

from sanic_ext import openapi

from ...caching import cacheResponse
from ...utils import dataclassResponse
from ..errors import PageNotFound
from ..extractors import home
from ..responses import Error, Ok, Recommendation


class Result(Ok):
    result: list[Recommendation]


@openapi.operation("home")
@openapi.summary("Inicio")
@openapi.description("### Obtem as recomendações da página inicial")
@openapi.parameter("page", int, description="Número da página", required=True, location="path")
@openapi.response(200, Result, "Retorna uma lista de recomendações")
@openapi.response(404, Error, "Página {page} não encontrada")
@cacheResponse(300)
@dataclassResponse
async def handler(_, page: int):
    try:
        results = await home.getPage(page)
    except PageNotFound:
        return Error(f"Page {page} not found!"), 404
    except Exception as e:
        logging.exception(
            f"Error on page {page} of home: %s", e,
            stack_info=True
        )
        return Error(f"Internal server error!"), 500
    return Result(results), 200
