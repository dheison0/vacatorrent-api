import logging
from . import (
    server, v1,
    PORT, DEBUG
)


v1.routes.add_to_server(server)

if DEBUG:
    logging.basicConfig(level=logging.INFO)

server.run('0.0.0.0', PORT, debug=DEBUG)
