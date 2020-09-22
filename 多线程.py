# -*- encoding: utf-8 -*-
#@Time: 9:07
#@Author:龙俊威
#@File:多线程.py
#@Software:PyCharm
import requests
from lxml import etree
import threading
from queue import Queue
import csv
import random
import datetime
import re
import xlwt
commodity_id = []
name_price = []
def get_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    ]
    user_agent = random.choice(user_agents)  # random.choice(),从列表中随机抽取一个对象
    return user_agent
class BSSpider(threading.Thread):
    ua = get_ua()
    headers = {
        'User-Agent': ua,
        'Connection': 'close'
    }
    def __init__(self,page_queue,data_queue,*args,**kwargs):
        super(BSSpider,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            response = requests.get(url, headers=self.headers, timeout=500).text
            selector = etree.HTML(response)
            # 最低价格
            lower_spice = selector.xpath('//script[@id="market_min_price_pat"]/text()')
            lower_spice = str(lower_spice)
            lower_spice = re.findall(r'<span class="custom-currency" data-price="(.*)" data-type="small" data-original-currency="CNY" ></span>',lower_spice)
            #饰品名
            ornaments_name = selector.xpath('//span[@class="cru-goods"]/text()')
            print(ornaments_name,lower_spice)
            # 写入data_queue
            self.data_queue.put((ornaments_name[0],lower_spice[0]))

class BSWriter(threading.Thread):
    def __init__(self,data_queue,writer,gLock,*args,**kwargs):
        super(BSWriter, self).__init__(*args,**kwargs)
        self.data_queue = data_queue
        self.writer = writer
        self.gLock = gLock

    def run(self):
        while True:
            try:
                data_info = self.data_queue.get()
                name,price = data_info
                self.gLock.acquire()
                self.writer.writerow((name,price))
                self.gLock.release()
                print('保存一条')
            except:
                break


def main():
    page_queue = Queue()
    data_queue = Queue()
    gLock = threading.Lock()
    # 获取当前时间
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%Y-%m-%d")
    fp = open('./data/{}.csv'.format(time_str), 'a+', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('名称', '价格'))

    file = open('input.txt')
    for line in file.readlines():
        line = line.strip()
        commodity_id.append(line)
    for item in commodity_id:
        url = 'https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling'.format(item)
        page_queue.put(url)

    for x in range(1,16):
        t = BSSpider(page_queue, data_queue)
        t.start()
    for x in range(1,16):
        t = BSWriter(data_queue,writer,gLock)
        t.start()
if __name__ == '__main__':
    main()