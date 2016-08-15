# -*- coding: utf-8 -*-
import os
from updateItemList import updateItemListThread

def updateAll():
    for fileName in os.listdir('data'):
        if os.path.isfile('data/' + fileName):
            args = fileName.strip('.json').split(' ')
            update_thread = updateItemListThread(user_id=args[0],
                                                 object_type=args[1],
                                                 group_type=args[2],
                                                 order_by=args[3])
            update_thread.start()

if __name__ == '__main__':
    updateAll()
