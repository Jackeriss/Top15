from tornado import httpserver, ioloop
from tornado.options import options
from app import create_app

if __name__ == '__main__':
    http_server = httpserver.HTTPServer(create_app())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
