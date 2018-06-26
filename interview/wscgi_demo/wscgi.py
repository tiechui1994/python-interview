from wsgiref.simple_server import make_server
from interview.wscgi_demo.application import application

http = make_server('', 8000, application)
http.serve_forever()
