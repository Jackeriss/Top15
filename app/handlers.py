import os
import json
from datetime import datetime

from tornado import web, gen, escape
from tornado.options import options

from .spider import grab


class PageNotFoundHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('error.html', code='404')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class IndexHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('index.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class IframeHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        arguments = {}
        arguments['user_id'] = self.get_argument('user_id', default=0)
        arguments['object_type'] = self.get_argument('object_type', default=0)
        arguments['group_type'] = self.get_argument('group_type', default=0)
        arguments['order_by'] = self.get_argument('order_by', default=0)
        arguments['tag'] = self.get_argument('tag', default=0)
        self.render('iframe.html', arguments=arguments)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')

class SpiderHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        feedback = 'wait'
        user_id = self.get_argument('user_id', default=0)
        object_type = self.get_argument('object_type', default=0)
        group_type = self.get_argument('group_type', default=0)
        order_by = self.get_argument('order_by', default=0)
        tag = self.get_argument('tag', default=0)
        key = ' '.join((user_id, object_type, group_type, order_by, tag))
        file_path = os.path.join(options.config['root_path'], 'data', key + '.json')
        handling = options.handling
        if not os.path.exists(file_path):
            if key not in handling:
                yield grab(user_id=user_id, object_type=object_type,
                           group_type=group_type, order_by=order_by, tag=tag)
                options.handling.append(key)
        else:
            if key in handling:
                options.handling.remove(key)
            with open(file_path, 'r') as items_file:
                items = json.loads(items_file.read())
            if datetime.now().strftime('%Y-%m-%d') != items[0]:
                yield grab(user_id=user_id, object_type=object_type,
                           group_type=group_type, order_by=order_by, tag=tag)
            if len(items) <= 1:
                feedback = '404'
            else:
                feedback = items
        respon_json = escape.json_encode(feedback)
        self.write(respon_json)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')
