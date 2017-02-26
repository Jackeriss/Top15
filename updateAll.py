import os
from app import spider

def updateAll():
    for fileName in os.listdir('data'):
        if os.path.isfile('data/' + fileName):
            args = fileName.strip('.json').split(' ')
            spider.grab(*args)

if __name__ == '__main__':
    updateAll()
