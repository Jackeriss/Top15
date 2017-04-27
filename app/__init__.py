'''Initialize App'''
import os
from tornado import web
from tornado.options import define, options
from config import CONFIG
from .handlers import (PageNotFoundHandler,
                       IndexHandler,
                       IframeHandler,
                       SpiderHandler)


def create_app():
    '''Create APP'''
    options.parse_command_line()
    define(
        'port',
        default=CONFIG['PORT'],
        help='run on the given port',
        type=int)
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=CONFIG['DEBUG'],
        xsrf_cookies=True,
        cookie_secret=CONFIG['COOKIE_SECRET'],
        gzip=True,
    )
    app = web.Application([
        (r'/', IndexHandler),
        (r'/iframe', IframeHandler),
        (r'/spider', SpiderHandler),
        (r'/(robots\.txt)',
         web.StaticFileHandler,
         dict(path=settings['static_path'])),
        ('.*', PageNotFoundHandler)
        ], **settings)
    return app
