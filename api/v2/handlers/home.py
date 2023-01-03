from ..errors import PageNotFound
from ..responses import Response, Error
from ..extractors import home
from ...caching import cacheResponse
from ...utils import dataclassResponse
import logging


@cacheResponse(300)
@dataclassResponse
async def handler(_, page: int = 1):
    try:
        results = await home.getPage(page)
    except PageNotFound:
        return Error(f"Page {page} not found!"), 404
    except Exception as e:
        logging.exception(f"Error page {page} of home: %s", e, stack_info=True)
        return Error(f"Internal server error!"), 500
    return Response(results), 200
