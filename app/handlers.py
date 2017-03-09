import os
import json
from tornado import web, httpclient, gen, escape
from config import COMMON_CONFIG
from .spider import grab


class PageNotFoundHandler(web.RequestHandler):
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


class SpiderHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        feedback = 'wait'
        user_id = self.get_argument('user_id', default=0)
        object_type = self.get_argument('object_type', default=0)
        group_type = self.get_argument('group_type', default=0)
        order_by = self.get_argument('order_by', default=0)
        tag = self.get_argument('tag', default=0)
        filePath = os.path.join(COMMON_CONFIG.DATA_DIR, user_id + ' ' +\
            object_type + ' ' + group_type + ' ' + order_by + ' ' + tag + '.json')
        handling = COMMON_CONFIG.HANDLING.lrange('handling', 0, -1)
        if not os.path.exists(filePath):
            if filePath.encode('utf-8') not in handling:
                grab(user_id=user_id, object_type=object_type,\
                    group_type=group_type, order_by=order_by, tag=tag)
                COMMON_CONFIG.HANDLING.rpush('handling', filePath)
        else:
            if filePath.encode('utf-8') in handling:
                COMMON_CONFIG.HANDLING.lrem('handling', 1, filePath)
            with open(filePath, 'r') as itemsFile:
                items = json.loads(itemsFile.read())
            if items == 0:
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
