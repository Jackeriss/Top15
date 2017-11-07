import os
import ssl
import json
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
        options.config['root_path'], 'data',
        ' '.join((user_id, object_type, group_type, order_by, tag)) + '.json')
    client = httpclient.AsyncHTTPClient()
    items = [datetime.now().strftime('%Y-%m-%d')]
    try:
        response = yield safty_fetch(client.fetch(url,
                                                  method='GET',
                                                  headers=options.config['headers'],
                                                  ssl_options=ssl._create_unverified_context()))
    except Exception as err:
        options.config['root_logger'].error(err, exc_info=True)
        with open(file_path, 'w') as items_file:
            items_file.write(json.dumps(items))
    else:
        text = response.body
        soup = BeautifulSoup(text, 'lxml')
        if object_type == '1':
            books = soup.findAll('li', attrs={'class': 'subject-item'})
            links = [book.find('h2').find('a')['href'] for book in books]
            try:
                detail_responses = yield [safty_fetch(client.fetch(
                    link,
                    method='GET',
                    headers=options.config['headers'],
                    ssl_options=ssl._create_unverified_context()))
                                          for link in links]
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
            else:
                for i, detail_response in enumerate(detail_responses):
                    item_dict = {}
                    item_dict['link'] = links[i]
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
            links = [div.find('a')['href'] for div in divs]
            titles = [div.find('em').get_text().split('/')[0].strip()
                      for div in divs]
            try:
                detail_responses = yield [safty_fetch(client.fetch(
                    link,
                    method='GET',
                    headers=options.config['headers'],
                    ssl_options=ssl._create_unverified_context()))
                                          for link in links]
            except Exception as err:
                options.config['root_logger'].error(err, exc_info=True)
            else:
                for i, detail_response in enumerate(detail_responses):
                    item_dict = {}
                    item_dict['link'] = links[i]
                    item_dict['title'] = titles[i]
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

@gen.coroutine
def safty_fetch(fetch_routine):
    try:
        response = yield fetch_routine
    except Exception as err:
        raise gen.Return(err)
    else:
        raise gen.Return(response)
