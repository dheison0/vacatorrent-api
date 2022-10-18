from . import app, PORT
from .extractor import home

@app.get('/')
def index():
    results = home.getAll()
    return list(map(lambda r: r.dict(), results))

app.run(host="0.0.0.0", port=PORT)
