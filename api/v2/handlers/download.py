import logging

from sanic_ext import openapi

from ...caching import cache
from ...utils import dataclassResponse
from ..errors import PageNotFound
from ..extractors import download
from ..responses import Download, Error, Ok


class Result(Ok):
    result: Download


@openapi.operation("download")
@openapi.summary("Download")
@openapi.description("### Obtem as informações de download")
@openapi.parameter("path", str, description="Localização do item no site", location="path", required=True)
@openapi.response(200, Result, "Retorna as informações de download")
@openapi.response(404, Error, "Download não encontrado")
@cache(900)
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
    return Result(result), 200
