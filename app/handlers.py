import urllib
import json
import datetime
import time
import os
import json
import ssl
import redis
from bs4 import BeautifulSoup
from tornado import httpserver, ioloop, options, web, httpclient, gen, escape
from .qiniu_api import Qiniu
from config import COMMON_CONFIG


class PageNotFoundHandler(web.RequestHandler):
    def get(self):
        self.render('index.html', code='404')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('index.html', code='404')
        else:
            self.render('index.html', code='500')


class IndexHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        try:
            key = self.get_argument('key').strip()
        except:
            key = ''
        self.render('index.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class IframeHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        arguments = {}
        arguments['user_id'] = self.get_argument('user_id')
        arguments['object_type'] = self.get_argument('object_type')
        arguments['group_type'] = self.get_argument('group_type')
        arguments['order_by'] = self.get_argument('order_by')
        arguments['tag'] = self.get_argument('tag')
        if arguments['tag'] == '':
            arguments['tag'] = '0'
        self.render('iframe.html', arguments=arguments)


class SpiderHandler(web.RequestHandler):
    @gen.coroutine
    def post(self):
        feedback = 'wait'
        user_id = self.get_argument('user_id')
        object_type = self.get_argument('object_type')
        group_type = self.get_argument('group_type')
        order_by = self.get_argument('order_by')
        tag = self.get_argument('tag')
        if tag == '':
            tag = '0'
        filePath = os.path.join(COMMON_CONFIG.DATA_DIR, user_id + ' ' + object_type + ' ' + group_type + ' ' + \
            order_by + ' ' + tag + '.json')
        handling = COMMON_CONFIG.HANDLING.lrange('handling', 0, -1)
        filePath
        if not os.path.exists(filePath):
            if filePath.encode('utf-8') not in handling:
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
                    tag_name = tag
                url = 'https://' + object_type_name + '.douban.com/people/' + \
                    user_id + '/' + group_type_name + '?sort=' + order_by_name + \
                    '&tag=' + tag_name
                client = httpclient.AsyncHTTPClient()
                try:
                    response = yield client.fetch(url, method='GET', headers=COMMON_CONFIG.HEADERS)
                except:
                    with open(filePath, 'w') as itemsFile:
                        itemsFile.write('0')
                else:
                    text = response.body
                    soup = BeautifulSoup(text, 'lxml')
                    resultList = soup.findAll('h3', attrs={'class':'t'})
                    items = []
                    existList = str(Qiniu().list_file_from_qiniu())
                    if object_type == '1':
                        books = soup.findAll('li', attrs={'class':'subject-item'})
                        for book in books:
                            itemDict = {}
                            itemDict['link'] = book.find('h2').find('a')['href']
                            try:
                                detailResponse = yield client.fetch(itemDict['link'], method='GET', headers=COMMON_CONFIG.HEADERS)
                            except:
                                pass
                            else:
                                detailText = detailResponse.body
                                detailSoup = BeautifulSoup(detailText, 'lxml')
                                itemDict['title'] = detailSoup.find('span', attrs={'property':'v:itemreviewed'}).get_text()
                                itemDict['rating'] = detailSoup.find('strong', attrs={'class':'rating_num'}).get_text()
                                src = detailSoup.find('img', attrs={'rel':'v:photo'})['src']
                                imageFileName = src.split('/')[-1]
                                itemDict['image'] = 'https://ocg2nnfbz.qnssl.com/images/' + imageFileName
                                items.append(itemDict)
                                if 'mpic' in src:
                                    imageURL = 'https://img3.doubanio.com/lpic/' + imageFileName
                                else:
                                    imageURL = 'https://img3.doubanio.com/view/photo/photo/public/' + imageFileName
                                if imageFileName not in existList:
                                    Qiniu.fetch_file_to_qiniu(url=imageURL, filename=imageFileName, path='images')
                    else:
                        divs = soup.findAll('div', attrs={'class':'item'})
                        for div in divs:
                            itemDict = {}
                            itemDict['title'] = div.find('em').get_text().split('/')[0].strip()
                            itemDict['link'] = div.find('a')['href']
                            try:
                                detailResponse = yield client.fetch(itemDict['link'], method='GET', headers=COMMON_CONFIG.HEADERS)
                            except:
                                pass
                            else:
                                detailText = detailResponse.body
                                detailSoup = BeautifulSoup(detailText, 'lxml')
                                itemDict['rating'] = detailSoup.find('strong', attrs={'class':'rating_num'}).get_text()
                                src = div.find('img')['src']
                                imageFileName = src.split('/')[-1]
                                itemDict['image'] = 'https://ocg2nnfbz.qnssl.com/images/' + imageFileName
                                items.append(itemDict)
                                if 'spic' in src:
                                    imageURL = 'https://img3.doubanio.com/lpic/' + imageFileName
                                else:
                                    imageURL = 'https://img3.doubanio.com/view/photo/photo/public/' + imageFileName
                                if imageFileName not in existList:
                                    Qiniu.fetch_file_to_qiniu(url=imageURL, filename=imageFileName, path='images')
                    with open(filePath, 'w') as itemsFile:
                        itemsFile.write(json.dumps(items))
                COMMON_CONFIG.HANDLING.rpush('handling', filePath)
        else:
            if filePath.encode('utf-8') in handling:
                COMMON_CONFIG.HANDLING.lrem('handling', 1, filePath)
            with open(filePath, 'r') as itemsFile:
                items = json.loads(itemsFile.read())
            if items == 0:
                feedback = '404'
            else:
                feedback = items
        respon_json = escape.json_encode(feedback)
        self.write(respon_json)
