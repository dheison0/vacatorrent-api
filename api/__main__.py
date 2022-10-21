from . import app, extractors, PORT


@app.get('/')
def home_page():
    try:
        recommendations = extractors.home.get_all()
    except Exception as error:
        result = {
            'ok': False,
            'error': f'failed to get homepage recommendations: {error}'
        }
    else:
        result = {
            'ok': True,
            'results': list(map(lambda r: r.dict(), recommendations))
        }
    return result


@app.get('/search/<string:query>')
@app.get('/search/<string:query>/<int:page>')
def search(query: str, page: int = 1):
    try:
        search_results, has_next = extractors.search.get_results(query, page)
    except Exception as error:
        result = {'ok': False, 'error': f'failed to search: {error}'}
    else:
        result = {
            'ok': True,
            'page': {
                'number': page,
                'has_next': has_next
            },
            'results': list(map(lambda r: r.dict(), search_results))
        }
    return result


@app.get('/get/<string:name>')
def get_download(name: str):
    return extractors.download.get_download(name).dict()


app.run(host="0.0.0.0", port=PORT)
