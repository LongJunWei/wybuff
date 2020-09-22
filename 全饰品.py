#-*- codeing = utf-8 -*-
#@Time: 14:15
#@Author:龙俊威
#@File:全饰品.py
#@Software:PyCharm

import requests
import re
import pandas as pd
import datetime
import time
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'Device-Id=mAA1NBaLyKiLMIXiKMzE; _ga=GA1.2.1009211001.1595470266; Locale-Supported=zh-Hans; game=csgo; _gid=GA1.2.224757453.1595729757; _gat_gtag_UA_109989484_1=1; NTES_YD_SESS=jH9Y.azrhZCn7tIq6daDcr8OheKkNTEg7ItCbW8BbMevrOhUrIJ5Lfqn2Xe07tgjTvN19hm3V2TN5KcZnjfIKk2LpEHhdvtcU3yEKBxZJxHjB8OLmI840NqX03V1.qc.i9DW9AVLxv1jts5VSYpKd1K3VCjYNT0nxI_EACjuWmtnENMpqRNa9RRMoZkz5hvSYPE5cnrXxqtauUhe0AP_abQMM02xXDZcEn0kf0mIm2gAQ; S_INFO=1595742058|0|3&80##|18971420284; P_INFO=18971420284|1595742058|1|netease_buff|00&99|null&null&null#hub&420000#10#0|&0||18971420284; session=1-6EVm2X4ypbtRT4XgQeu7QpL-KsB7l3jh7sy8m4xB6SdY2044135696; csrf_token=IjQxMjdkZWE1MzBlZWNiMjAxMjkwZGJjMTllZjQzMzFmNzQ2ODY4ZjYi.Ef6o8w.HSdNOJIIUGjhuhTqfh7cr_5x5Gk',
    'Host':'buff.163.com',
    'Referer':'https://buff.163.com/market/?game=csgo',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}
def main():
    # 获取当前时间
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%Y-%m-%d")
    start_url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1'
    max_page = get_max_page(start_url)
    max_page = int(max_page)
    #遍历所有页
    for index in range(0,max_page):
        time.sleep(1)
        url = 'https://buff.163.com/api/market/goods?game=csgo&page_num={}'.format(index+1)
        print('正在爬取:{}'.format(url))
        get_name_price(url,time_str)
def get_name_price(url,time):
    html = requests.get(url=url, headers=headers).text
    names = re.findall(r'"market_hash_name": "(.*?)"', html)
    prices = re.findall(r'"sell_min_price": "(.*?)"', html)
    data = list(map(lambda x: (time,names[x], prices[x]), range(len(names))))
    result = pd.DataFrame(data)
    result.to_csv('./全饰品/{}全饰品价格.csv'.format(time),index = False,header=0,mode='a+')
def get_max_page(start_url):
    html = requests.get(url=start_url, headers=headers).text
    max_page = re.findall(r'"total_page":(.*)', html)[0].strip(' ')
    return max_page

if __name__ == '__main__':
    main()