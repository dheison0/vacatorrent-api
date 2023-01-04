from os import getenv
from textwrap import dedent

from sanic import Sanic

SITE_URL = 'https://vacatorrent.com'
PORT = int(getenv("PORT", "5000"))

server = Sanic('VacaTorrent')
server.ext.openapi.describe(
    "VacaTorrent",
    version="2.0",
    description=dedent("""
        API para extração de filmes, séries e desenhos do site [VacaTorrent]
        criada usando [Python], [Sanic] e [BeautifulSoup4]

        Código fonte disponivel no github: [dheisom/vacatorrent-api]  
        Um aplicativo construido encima da API também está disponivel no github: [dheisom/VacaTorrent]

        [VacaTorrent]: <https://vacatorrent.com>
        [Python]: <https://python.org>
        [Sanic]: <https://sanic.dev>
        [BeautifulSoup4]: <https://beautiful-soup-4.readthedocs.io/en/latest>
        [dheisom/vacatorrent-api]: <https://github.com/dheisom/vacatorrent-api>
        [dheisom/VacaTorrent]: <https://github.com/dheisom/VacaTorrent>
    """)
)