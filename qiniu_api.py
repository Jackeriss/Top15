# -*- coding: utf-8 -*-
from qiniu import Auth, put_data, BucketManager
import os
import uuid

ACCESS_KEY = ''# Use your own
SECRET_KEY = ''# Use your own
BUCKET_NAME = ''# Use your own
q = Auth(ACCESS_KEY, SECRET_KEY)


class Qiniu(object):
    def save_file_to_qiniu(self,
                           upload_file,
                           filename=str(uuid.uuid1()).replace('-', ''),
                           path='attach'):
        try:
            key = '%s/%s' % (path, filename)
            token = self.q.upload_token(BUCKET_NAME, key)
            ret, info = put_data(token, key, upload_file)
            if ret.get('key', None) == None:
                raise Exception('upload error')
            else:
                return u'%s' % key
        except Exception, e:
            print(str(e))
            return str(e)

    def fetch_file_to_qiniu(self,
                            url,
                            filename=str(uuid.uuid1()).replace('-', ''),
                            path='attach'):
        try:
            key = '%s/%s' % (path, filename)
            bucket = BucketManager(q)
            ret, info = bucket.fetch(url, BUCKET_NAME, key)
            if ret.get('key', None) == None:
                raise Exception('fetch error')
            else:
                return u'%s' % key
        except Exception, e:
            print(str(e))
            return str(e)

    def list_file_from_qiniu(self):
        info = None
        prefix = 'images'
        limit = None
        delimiter = None
        marker = None
        try:
            bucket = BucketManager(q)
            ret, eof, info = bucket.list(BUCKET_NAME, prefix, marker, limit, delimiter)
        except Exception, e:
            pass
        finally:
            return info
