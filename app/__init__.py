'''Initialize App'''
import os
import redis
from tornado import web
from tornado.options import define, options
from config import DEV_CONFIG, PROD_CONFIG
from .handlers import (PageNotFoundHandler,
                       IndexHandler,
                       IframeHandler,
                       SpiderHandler)


def create_app():
    '''Create APP'''
    define(
        'config',
        default='dev',
        help='[dev|prod](dev is defualt)',
        type=str)
    options.parse_command_line()
    if options.config == 'dev':
        DEV_CONFIG['HANDLING'] = redis.StrictRedis(host=DEV_CONFIG['REDIS_HOST'],
                                                   port=DEV_CONFIG['REDIS_PORT'], db=0)
        DEV_CONFIG['HANDLING'].flushdb()
        define(
            'CONFIG',
            default=DEV_CONFIG,
            type=dict)
    else:
        PROD_CONFIG['HANDLING'] = redis.StrictRedis(host=PROD_CONFIG['REDIS_HOST'],
                                                    port=PROD_CONFIG['REDIS_PORT'], db=0)
        PROD_CONFIG['HANDLING'].flushdb()
        define(
            'CONFIG',
            default=PROD_CONFIG,
            type=dict)
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=options.CONFIG['DEBUG'],
        xsrf_cookies=True,
        cookie_secret=options.CONFIG['COOKIE_SECRET'],
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
