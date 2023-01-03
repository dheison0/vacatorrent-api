import logging

from ...caching import cacheResponse
from ...utils import dataclassResponse
from ..extractors import search
from ..errors import PageNotFound, NoResults
from ..responses import Error, Response
from sanic.request import Request


@cacheResponse(900)
@dataclassResponse
async def handler(req: Request, query: str):
    page = int(req.args.get('page', 1), 10)
    try:
        result = await search.getResults(query, page)
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
    return Response(result), 200
