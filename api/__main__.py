from . import app, routes, PORT

routes.add_all(app)

app.run(host="0.0.0.0", port=PORT)
