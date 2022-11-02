from . import app, routes, PORT

routes.add_all(app)

app.run('0.0.0.0', PORT)
