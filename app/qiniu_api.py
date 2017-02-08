import os
import uuid
from qiniu import Auth, put_data, BucketManager
from config import COMMON_CONFIG


q = Auth(COMMON_CONFIG.ACCESS_KEY, COMMON_CONFIG.SECRET_KEY)


class Qiniu(object):
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
                return '%s' % key
        except Exception as e:
            print (str(e))
            return str(e)

    def list_file_from_qiniu(self):
        info = None
        prefix = 'images'
        limit = None
        delimiter = None
        marker = None
        try:
            bucket = BucketManager(q)
            ret, eof, info = bucket.list(COMMON_CONFIG.BUCKET_NAME, prefix, marker, limit, delimiter)
        except Exception as e:
            pass
        finally:
            return info
