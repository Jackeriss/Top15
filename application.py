'''da'''
from tornado import httpserver, ioloop
from tornado.options import options
from app import create_app

if __name__ == '__main__':
    HTTP_SERVER = httpserver.HTTPServer(create_app())
    HTTP_SERVER.listen(options.port)
    ioloop.IOLoop.instance().start()
