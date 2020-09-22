#-*- codeing = utf-8 -*-
#@Time: 17:24
#@Author:龙俊威
#@File:读取txt文件.py
#@Software:PyCharm

def not_empty(s):
    return s and s.strip()

file=open('id.txt')
datalist = []
for line in file.readlines():
    curLine=line.strip().split(" ")

result = list(filter(not_empty, curLine))
lenth = len(result)
print(lenth)
with open('result.txt','w') as f:
    for le in range(lenth):
        f.write(result[le]+'\n')
    # floatLine=list(map(float,curLine))#这里使用的是map函数直接把数据转化成为float类型
    # dataMat.append(floatLine[0:2])
# print(dataMat)
