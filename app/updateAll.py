import os
from updateItemList import updateItemListThread

def updateAll():
    for fileName in os.listdir('data'):
        if os.path.isfile('data/' + fileName):
            args = fileName.strip('.json').split(' ')
            update_thread = updateItemListThread(*args)
            update_thread.start()

if __name__ == '__main__':
    updateAll()
