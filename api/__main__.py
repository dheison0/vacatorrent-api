from . import PORT, server, v2

v2.addRoutesToServer(server)

server.run('0.0.0.0', port=PORT)
