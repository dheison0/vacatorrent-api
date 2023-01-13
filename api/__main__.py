from . import PORT
from . import caching, server, v2

v2.addRoutesToServer(server)

@server.listener("after_server_start")
async def afterStart(*_):
    caching.start()

@server.listener("before_server_stop")
async def beforeStop(*_):
    caching.stop()

server.run('0.0.0.0', port=PORT)
