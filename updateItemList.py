# -*- coding: utf-8 -*-
import urllib2
import os
import requests
import threading
import json
from bs4 import BeautifulSoup
from qiniu_api import Qiniu
from key import HEADERS

class updateItemListThread (threading.Thread):
    def __init__(self, user_id, object_type, group_type, order_by, tag):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.object_type = object_type
        self.group_type = group_type
        self.order_by = order_by
        self.tag = tag
        self.id = self.user_id + ' ' + self.object_type + ' ' + self.group_type + \
            ' ' + self.order_by + ' ' + self.tag
        object_type_name = '0'
        group_type_name = '0'
        order_by_name = '0'
        if object_type == '0':
            object_type_name = 'movie'
        elif object_type == '1':
            object_type_name = 'book'
        elif object_type == '2':
            object_type_name = 'music'
        if group_type == '0':
            group_type_name = 'collect'
        elif group_type == '1':
            group_type_name = 'wish'
        elif group_type == '2':
            group_type_name = 'do'
        if order_by == '0':
            order_by_name = 'time'
        elif order_by == '1':
            order_by_name = 'rating'
        if tag == '0':
            tag_name = ''
        else:
            tag_name = tag.encode('utf-8')
        self.url = 'https://' + object_type_name + '.douban.com/people/' + \
            user_id + '/' + group_type_name + '?sort=' + order_by_name + \
            '&tag=' + tag_name
    def run(self):
        self.updateItemList()

    def updateItemList(self):
        try:
            req = urllib2.Request(self.url, headers=HEADERS)
            text = urllib2.urlopen(req).read()
            soup = BeautifulSoup(text, 'html.parser')
        except:
            with open('data/' + self.id + '.json', 'w') as itemsFile:
                itemsFile.write('0')
        else:
            items = []
            existList = str(Qiniu().list_file_from_qiniu())
            if self.object_type == '1':
                books = soup.findAll('li', attrs={'class':'subject-item'})
                for i in range(0, len(books)):
                    itemDict = {}
                    itemDict['link'] = books[i].find('h2').find('a')['href']
                    reqDetail = urllib2.Request(itemDict['link'])
                    textDetail = urllib2.urlopen(reqDetail).read()
                    soupDetail = BeautifulSoup(textDetail, 'html.parser')
                    itemDict['title'] = soupDetail.find('span', attrs={'property':'v:itemreviewed'}).get_text()
                    itemDict['rating'] = soupDetail.find('strong', attrs={'class':'rating_num'}).get_text()
                    src = soupDetail.find('img', attrs={'rel':'v:photo'})['src']
                    imageFileName = src.split('/')[-1]
                    itemDict['image'] = 'https://ocg2nnfbz.qnssl.com/images/' + imageFileName
                    items.append(itemDict)
                    if 'mpic' in src:
                        imageURL = 'https://img3.doubanio.com/lpic/' + imageFileName
                    else:
                        imageURL = 'https://img3.doubanio.com/view/photo/photo/public/' + imageFileName
                    if imageFileName not in existList:
                        Qiniu().fetch_file_to_qiniu(url=imageURL, filename=imageFileName, path='images')
            else:
                divs = soup.findAll('div', attrs={'class':'item'})
                for i in range(0, len(divs)):
                    itemDict = {}
                    itemDict['title'] = divs[i].find('em').get_text().split('/')[0].strip()
                    itemDict['link'] = divs[i].find('a')['href']
                    reqDetail = urllib2.Request(itemDict['link'])
                    textDetail = urllib2.urlopen(reqDetail).read()
                    soupDetail = BeautifulSoup(textDetail, 'html.parser')
                    itemDict['rating'] = soupDetail.find('strong', attrs={'class':'rating_num'}).get_text()
                    src = divs[i].find('img')['src']
                    imageFileName = src.split('/')[-1]
                    itemDict['image'] = 'https://ocg2nnfbz.qnssl.com/images/' + imageFileName
                    items.append(itemDict)
                    if 'spic' in src:
                        imageURL = 'https://img3.doubanio.com/lpic/' + imageFileName
                    else:
                        imageURL = 'https://img3.doubanio.com/view/photo/photo/public/' + imageFileName
                    if imageFileName not in existList:
                        Qiniu().fetch_file_to_qiniu(url=imageURL, filename=imageFileName, path='images')
            with open('data/' + self.id + '.json', 'w') as itemsFile:
                itemsFile.write(json.dumps(items))
