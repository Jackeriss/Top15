import os
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from tornado import httpclient, gen
from tornado.options import options


@gen.coroutine
def grab(user_id, object_type, group_type, order_by, tag):
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
    file_path = os.path.join(
        options.CONFIG['DATA_DIR'], user_id + ' ' + object_type + ' ' +
        group_type + ' ' + order_by + ' ' + tag + '.json')
    client = httpclient.AsyncHTTPClient()
    try:
        response = yield client.fetch(url,
                                      method='GET',
                                      headers=options.CONFIG['HEADERS'])
        print(1)
    except Exception as _e:
        print(2)
        print(_e)
        with open(file_path, 'w') as items_file:
            items_file.write('0')
    else:
        print(3)
        text = response.body
        soup = BeautifulSoup(text, 'lxml')
        items = [datetime.now().strftime('%Y-%m-%d')]
        if object_type == '1':
            books = soup.findAll('li', attrs={'class': 'subject-item'})
            for book in books:
                item_dict = {}
                item_dict['link'] = book.find('h2').find('a')['href']
                try:
                    detail_response = yield client.fetch(
                        item_dict['link'],
                        method='GET',
                        headers=options.CONFIG['HEADERS'])
                except Exception as _e:
                    print(_e)
                else:
                    detail_text = detail_response.body
                    detail_soup = BeautifulSoup(detail_text, 'lxml')
                    item_dict['title'] = detail_soup.find(
                        'span',
                        attrs={'property': 'v:itemreviewed'}).get_text()
                    item_dict['rating'] = detail_soup.find(
                        'strong', attrs={'class': 'rating_num'}).get_text()
                    item_dict['image'] = detail_soup.find(
                        'img', attrs={'rel': 'v:photo'})['src']
                    items.append(item_dict)
        else:
            divs = soup.findAll('div', attrs={'class': 'item'})
            for div in divs:
                item_dict = {}
                item_dict['title'] = div.find('em').get_text().split('/')[0].\
                    strip()
                item_dict['link'] = div.find('a')['href']
                try:
                    detail_response = yield client.fetch(
                        item_dict['link'],
                        method='GET',
                        headers=options.CONFIG['HEADERS'])
                except Exception as _e:
                    print(_e)
                else:
                    detail_text = detail_response.body
                    detail_soup = BeautifulSoup(detail_text, 'lxml')
                    item_dict['rating'] = detail_soup.find(
                        'strong', attrs={'class': 'rating_num'}).get_text()
                    if object_type == '0':
                        item_dict['image'] = detail_soup.find(
                            'img', attrs={'rel': 'v:image'})['src']
                    else:
                        item_dict['image'] = detail_soup.find(
                            'img', attrs={'rel': 'v:photo'})['src']
                    items.append(item_dict)
        with open(file_path, 'w') as items_file:
            items_file.write(json.dumps(items))
