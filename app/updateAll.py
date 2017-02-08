import os
from spider import grab

def updateAll():
    for fileName in os.listdir('data'):
        if os.path.isfile('data/' + fileName):
            args = fileName.strip('.json').split(' ')
            grab(*args)

if __name__ == '__main__':
    updateAll()
