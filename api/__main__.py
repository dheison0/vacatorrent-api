from . import app, PORT
from . import v1
from os import getenv

v1.routes.registry(app)

app.run('0.0.0.0', PORT, debug=getenv("DEBUG") != None)
