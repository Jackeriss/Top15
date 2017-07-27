'''Config'''
import os
import copy

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

COMMON_CONFIG = {
    'port': 8082,
    'debug': True,
    'root_path': ROOT_PATH,
    'headers': {'cookie': ('ll="118348"; bid=u7DQ-3A5QCo; ps=y; ue="1075704670'
                           '@qq.com"; dbcl2="63626550:zAz6Nxzch4M"; ck=B1MZ; c'
                           't=y; ap=1; push_noty_num=0; push_doumail_num=0')}}

DEV_CONFIG = copy.deepcopy(COMMON_CONFIG)

PROD_CONFIG = copy.deepcopy(COMMON_CONFIG)
PROD_CONFIG['debug'] = False
