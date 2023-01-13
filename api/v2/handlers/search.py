import logging
from dataclasses import dataclass
from urllib.parse import unquote

from sanic.request import Request
from sanic_ext import openapi

from ...caching import cache
from ...utils import dataclassResponse
from ..errors import NoResults, PageNotFound
from ..extractors import search
from ..responses import Error, Ok, SearchResult


@dataclass
class Result(Ok):
    result: list[SearchResult]
    has_more: bool


@openapi.operation("search")
@openapi.summary("Procurar")
@openapi.description("### Procurar por filmes, séries e desenhos")
@openapi.parameter('query', str, description="O que você deseja procurar", required=True)
@openapi.parameter('page', int, description="Número da página")
@openapi.response(200, Result, "Retorna a lista de items encontrados")
@openapi.response(400, Error, "Página {page} da pesquisa não encontrada")
@openapi.response(418, Error, "Nenhum resultado foi encontrado")
@cache(900)
@dataclassResponse
async def handler(req: Request):
    query = req.args.get("query")
    if not query:
        return Error("query not specified"), 400
    query = unquote(query)
    page = int(req.args.get('page', 1))
    try:
        result, hasNextPage = await search.getResults(query, page)
    except NoResults:
        return Error(f"Sorry, we not found any result for your query."), 200
    except PageNotFound:
        return Error(f"Page {page} of query '{query}' not found!"), 400
    except Exception as e:
        logging.exception(
            f"Error on search for '{query}': %s", e,
            stack_info=True
        )
        return Error("Internal server error!"), 500
    return Result(result, hasNextPage), 200
