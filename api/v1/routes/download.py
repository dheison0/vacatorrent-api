from http import HTTPStatus
from logging import error, info
from sanic import json
from ..extractors import download as download_extractor
from ...utils import log_exception


async def handler(_, key: str):
    "Obtem as informações de download de um filme/serie"
    try:
        result = await download_extractor.get_download(key)
    except Exception as err:
        error("Download: params: key='%s'", key)
        log_exception(err)
        return json(
            body={'error': f'failed to get download informations: {str(err)}'},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return json(body=result.dict(), status=HTTPStatus.OK)
