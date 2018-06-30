def application(environ, start_response):
    response_header = [('Content-Type', 'text/html')]
    start_response('200 OK', response_header)

    return [b'<h1>Hello web</h1>']

