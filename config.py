import os
import redis

basedir = os.path.abspath(os.path.dirname(__file__))


class COMMON_CONFIG:
    PORT = 8082
    DEBUG = True
    DATA_DIR = os.path.join(basedir, 'data')
    COOKIE_SECRET = 'oqA/6vVxSu6IU+5UErK21/yv7XHASUwap+0z6WL3TJQ='
    ACCESS_KEY = 'xyB8wvoj4mZRHFrhFgkcuJUPMjjeyN2uoTmBNOMK'
    SECRET_KEY = '1eDmF903TifW7BmuusF-DGWoVut3wqhxbdnIi2yB'
    BUCKET_NAME = 'top15'
    HEADERS = {'cookie': 'll="118348"; bid=GHivBqEUNvk; ps=y; ct=y; vtd-d="1"; ap=1;\
     ue="1075704670@qq.com"; dbcl2="63626550:qq6zQYSLKlw"; ck=zCRQ; push_noty_num=0\
     ; push_doumail_num=0'}
    HANDLING = redis.StrictRedis(host='redis', port=6379, db=0)
    # HANDLING = redis.StrictRedis(host='localhost', port=6379, db=0)
