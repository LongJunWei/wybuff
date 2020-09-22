#-*- codeing = utf-8 -*-
#@Time: 9:45
#@Author:龙俊威
#@File:spideer.py
#@Software:PyCharm
import datetime
import requests
from lxml import etree
import xlwt
import re
import time
import random
import pymongo
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

commodity_id = []
name_price = []

def main():
    # 链接数据库
    client = pymongo.MongoClient()
    nameandprice = client.buff.price
    #从txt中获取每一行数据
    file = open('input.txt')
    for line in file.readlines():
        line = line.strip()
        commodity_id.append(line)
    #获取当前时间
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%Y-%m-%d")
    #查找数据库中是否已经有这一天的数据
    jud = nameandprice.find_one({'时间':time_str},{'_id':0})
    #如果jud为空
    if not jud:
        #得到饰品名称
        for item in commodity_id:
            url = 'https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling'.format(item)
            get_name_spice(url,time_str,nameandprice)
            print(url)
        strr = "./data/" + time_str + ".xls"
        save_data(name_price,strr,time_str)
        client.close()
    else:
        # 得到饰品名称
        for item in commodity_id:
            url = 'https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling'.format(item)
            upd_name_spice(url,time_str,nameandprice)
            print(url)
        strr = "./data/" + time_str + ".xls"
        save_data(name_price, strr, time_str)
        client.close()

#更新数据库中的数据
def upd_name_spice(url,time,dbs):
    print('执行更新操作')
    selector = comp(url)
    lower_spice = selector.xpath('//script[@id="market_min_price_pat"]/text()')
    lower_spice = str(lower_spice)
    lower_spice = re.findall(
        r'<span class="custom-currency" data-price="(.*)" data-type="small" data-original-currency="CNY" ></span>',
        lower_spice)
    ornaments_name = selector.xpath('//span[@class="cru-goods"]/text()')
    dbs.update_one({'时间':time,'饰品名称':ornaments_name[0]},{'$set':{'当前最低价格':lower_spice[0]}},upsert=True)
    data = [ornaments_name[0], lower_spice[0] + '元']
    print(data)
    name_price.append(data)
#如果数据库中没有这一天的数据则插入
def get_name_spice(url,time,dbs):
    print('执行插入操作')
    selector = comp(url)
    lower_spice = selector.xpath('//script[@id="market_min_price_pat"]/text()')
    lower_spice = str(lower_spice)
    lower_spice = re.findall(r'<span class="custom-currency" data-price="(.*)" data-type="small" data-original-currency="CNY" ></span>',lower_spice)
    ornaments_name = selector.xpath('//span[@class="cru-goods"]/text()')
    result = {'时间':time,'饰品名称':ornaments_name[0],'当前最低价格':lower_spice[0]}
    dbs.insert_one(result)
    data = [ornaments_name[0], lower_spice[0]+'元']
    print(data)
    name_price.append(data)

def comp(url):
    html = requests.get(url=url, headers=headers).text
    selector = etree.HTML(html)
    #查看获取的网页内容
    # selector = etree.tostring(selector, encoding='utf-8').decode('utf-8')
    # print(selector)
    return selector
#price是存放所有的数据的列表
def save_data(name_price,strr,name):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet(name, cell_overwrite_ok=True)
    col = ("饰品名字", "当前最低价格")
    for i in range(0, 2):
        worksheet.write(0, i, col[i])
    for i in range(len(name_price)):
        data = name_price[i]
        for j in range(0,2):
            worksheet.write(i+1,j,data[j])
    workbook.save(strr)


if __name__ == '__main__':
    main()