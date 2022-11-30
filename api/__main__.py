from . import app, PORT
from .v1 import routes as v1_routes
from os import getenv

v1_routes.registry(app)

app.run('0.0.0.0', PORT, debug=getenv("DEBUG") != None)
