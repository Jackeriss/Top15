from bs4 import BeautifulSoup
from tornado import httpserver, ioloop, options, web, httpclient, gen, escape
from qiniu_api import Qiniu
from config import COMMON_CONFIG

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
    client = httpclient.AsyncHTTPClient()
    print(url)
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
        existList = str(Qiniu.list_file_from_qiniu())
        if object_type == '1':
            books = soup.findAll('li', attrs={'class':'subject-item'})
            for book in books:
                itemDict = {}
                itemDict['link'] = book.find('h2').find('a')['href']
                reqDetail = urllib2.Request(itemDict['link'], headers=COMMON_CONFIG.HEADERS)
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
                    Qiniu.fetch_file_to_qiniu(url=imageURL, filename=imageFileName, path='images')
        else:
            divs = soup.findAll('div', attrs={'class':'item'})
            for div in divs:
                itemDict = {}
                itemDict['title'] = div.find('em').get_text().split('/')[0].strip()
                itemDict['link'] = div.find('a')['href']
                reqDetail = urllib2.Request(itemDict['link'], headers=COMMON_CONFIG.HEADERS)
                textDetail = urllib2.urlopen(reqDetail).read()
                soupDetail = BeautifulSoup(textDetail, 'html.parser')
                itemDict['rating'] = soupDetail.find('strong', attrs={'class':'rating_num'}).get_text()
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
        with open(filePath + '.json', 'w') as itemsFile:
            itemsFile.write(json.dumps(items))

grab(user_id='Jackeriss', object_type='0', group_type='0', order_by='1', tag='0')
