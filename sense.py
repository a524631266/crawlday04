#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Zhangll
@software: PyCharm Community Edition
@time: 2016/9/26 23:43
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#错误处理

import requests
from bs4 import BeautifulSoup
import json
import time
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('localhost', 27017)                 # 连接Mongodb数据库
sense = client['sense']                                          # 创建数据库
url_list = sense['url_list']                                     # 创建数据表
item_list=sense['item_list']
def get_city():
    # url="http://www.senseluxury.com/destinations/2"
    url="http://www.senseluxury.com/destnav"
    # url="http://www.senseluxury.com/destnav/1"
    response=requests.get(url)
    if response.status_code==404: ###返回404为服务无法返回数
        print('404erro')
    else:
        # print(response.text)
        soup=BeautifulSoup(response.text,"lxml")
        # lists=soup.find_all('dl','dl-list')
        lists=soup.find_all('a')
        data=[list1.get("href") for list1 in lists]
        item_list_data={"item":data}
        print item_list_data
        item_list.insert_one(item_list_data)
        # urls=soup.select("div > div > dl.dl-list> dd > a")
        return [list.get("href") for list in lists]
def get_city_urls():
    """获取首页所有城市的url列表"""
    with open('six.html') as f:
        response = f.read()                                      # 读取本地html文件
    soup = BeautifulSoup(response, 'lxml')
    urls = soup.select('#destination_nav > div > div > div > dl.dl-list > dt > a')

    return [url.get('href') for url in urls]                     # 列表解析式，存储各城市URL链接


def get_page_list(city, page=1):
    """获取列表页数据"""
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 创建时间
    try:
        url = 'http://www.senseluxury.com/destinations_list/%s?page=%s' % (city.split('/')[-1], page)
        response = requests.get(url)                                 # 发送请求
        wb_data = json.loads(response.text[1:-1])                    # 将JSON字符串转换为字典
        # print wb_data['val']

        # 循环获取键值数据
        for i in wb_data['val']['data']:
            title = i['title']
            url = 'http://www.senseluxury.com' + i['url']            # 拼接链接
            server = i['server'].replace('&nbsp;', ' ').split()      # 数据清理，替换脏数据
            img = i['imageUrl']
            memo = i['memo']
            price = i['price']
            address = i['address'].split()
            subject = i['subject']
            data = {'title': title, 'url': url, 'server': server, 'img': img, 'memo': memo,
                    'price': price, 'adderss': address, 'subject': subject, 'create_time': now}

            url_list.insert_one(data)                                # 将数据插入数据库
            print data
    except Exception,e:
            print Exception,e
def get_all_list(city):
    for page in range(1,3):
        get_page_list(city,page)

def func(x):
    try:
        return 1/x
    # except ZeroDivisionError,e:
    #     print(ZeroDivisionError,e)
    # except TypeError,e:
    #     print(TypeError,e)
    except Exception,e:
        print(Exception,e)

url_list_urls=set([i['url'] for i in url_list.find()])#set是字典数据不重复数据


if __name__ == '__main__':
    # get_page_list('http://www.senseluxury.com/destinations/25')
    # print get_city_urls()

    # city_urls = get_city()
    # pool = Pool(processes=1)                                     # 设置进程池中的进程数
    # pool.map(get_page_list, city_urls)                           # 将列表中的每个对象应用到get_page_list函数
    # pool.close()                                                 # 等待进程池中的进程执行结束后再关闭pool
    # # pool.join()                                                  # 防止主进程在子进程结束前提前关闭
    # get_city()
    itemdd=[i['item'] for i in item_list.find()]
    itemdd2=
    print [i['item'] for i in item_list.find()]

   # print  func(0)