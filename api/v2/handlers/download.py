import logging

from ...caching import cacheResponse
from ...utils import dataclassResponse
from ..errors import PageNotFound
from ..extractors import download
from ..responses import Error, Response


@cacheResponse(900)
@dataclassResponse
async def handler(_, path: str):
    try:
        result = await download.getDownload(path)
    except PageNotFound:
        return Error(f"Download of path {path} not found!"), 404
    except Exception as e:
        logging.exception(
            f"Error on download of {path}: %s", e,
            stack_info=True
        )
        return Error(f"Internal server error"), 500
    return Response(result), 200
