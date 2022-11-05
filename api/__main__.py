from . import app, routes, PORT
from os import getenv

routes.add_all(app)

app.run('0.0.0.0', PORT, debug=getenv("DEBUG") != None)
