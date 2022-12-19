from . import PORT, server, v1

v1.routes.add_to_server(server)

server.run('0.0.0.0', port=PORT)
