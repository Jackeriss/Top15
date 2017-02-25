import os
import time
from app import spider
from tornado import gen

@gen.coroutine
def updateAll():
    while 1:
        for fileName in os.listdir('data'):
            if os.path.isfile('data/' + fileName):
                args = fileName.strip('.json').split(' ')
                print(args)
                spider.grab(*args)
        time.sleep(86400)

if __name__ == '__main__':
    updateAll()
