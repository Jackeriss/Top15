'''Config'''
import os
import copy

BASEDIR = os.path.abspath(os.path.dirname(__file__))

COMMON_CONFIG = {
    'PORT': 8082,
    'DEBUG': True,
    'DATA_DIR': os.path.join(BASEDIR, 'data'),
    'COOKIE_SECRET': 'oqA/6vVxSu6IU+5UErK21/yv7XHASUwap+0z6WL3TJQ=',
    'HEADERS': {'cookie': ('ll="118348"; bid=u7DQ-3A5QCo; ps=y; ue="1075704670'
                           '@qq.com"; dbcl2="63626550:zAz6Nxzch4M"; ck=B1MZ; a'
                           'p=1; push_noty_num=0; push_doumail_num=0')},
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': 6379}

DEV_CONFIG = copy.deepcopy(COMMON_CONFIG)

PROD_CONFIG = copy.deepcopy(COMMON_CONFIG)
PROD_CONFIG['DEBUG'] = False
PROD_CONFIG['REDIS_HOST'] = 'redis'
