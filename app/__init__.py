import os
from tornado import web
from tornado.options import define, options
from .handlers import *
from config import COMMON_CONFIG

def create_app():
    options.parse_command_line()
    define('port', default=COMMON_CONFIG.PORT, help='run on the given port', type=int)
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=COMMON_CONFIG.DEBUG,
        xsrf_cookies=True,
        cookie_secret=COMMON_CONFIG.COOKIE_SECRET,
        gzip=True,
    )
    app = web.Application([
        (r'/', IndexHandler),
        (r'/iframe', IframeHandler),
        (r'/spider', SpiderHandler),
        ('.*', PageNotFoundHandler)
     ], **settings)
    return app
