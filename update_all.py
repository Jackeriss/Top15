'''Update all json file'''
import os
import time
from app import spider

def update_all():
    '''Update all json file'''
    for file_name in os.listdir('data'):
        if os.path.isfile('data/' + file_name):
            args = file_name.strip('.json').split(' ')
            spider.grab(*args)

if __name__ == '__main__':
    while 1:
        update_all()
        time.sleep(28800)
