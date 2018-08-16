import json
import ast
import time
from datetime import datetime, timedelta

file_object = open('historyorder.txt', 'r',encoding='utf-8')

validDate = {}

def process(request):
    if request == 0:
        if d['merchantShopId'] in validDate:
            if d['validDate'] == "一周":
                validDate[d['merchantShopId']] += timedelta(days=7)
            if d['validDate'] == "一个月":
                validDate[d['merchantShopId']] += timedelta(days=30)
            if d['validDate'] == "一季度":
                validDate[d['merchantShopId']] += timedelta(days=90)
            if d['validDate'] == "半年":
                validDate[d['merchantShopId']] += timedelta(days=180)
            if d['validDate'] == "一年":
                validDate[d['merchantShopId']] += timedelta(days=365)
        else:
            if d['validDate'] == "一周":
                validDate[d['merchantShopId']] = t1 + timedelta(days=7)
            if d['validDate'] == "一个月":
                validDate[d['merchantShopId']] = t1 + timedelta(days=30)
            if d['validDate'] == "一季度":
                validDate[d['merchantShopId']] = t1 + timedelta(days=90)
            if d['validDate'] == "半年":
                validDate[d['merchantShopId']] = t1 + timedelta(days=180)
            if d['validDate'] == "一年":
                validDate[d['merchantShopId']] = t1 + timedelta(days=365)
    else:
        if d['validDate'] == "一周":
            validDate[d['merchantShopId']] = t1 + timedelta(days=7)
        if d['validDate'] == "一个月":
            validDate[d['merchantShopId']] = t1 + timedelta(days=30)
        if d['validDate'] == "一季度":
            validDate[d['merchantShopId']] = t1 + timedelta(days=90)
        if d['validDate'] == "半年":
            validDate[d['merchantShopId']] = t1 + timedelta(days=180)
        if d['validDate'] == "一年":
            validDate[d['merchantShopId']] = t1 + timedelta(days=365)

while True:
    line = file_object.readline()
    if not line:
        break
    d = ast.literal_eval(line)
    # print(d)
    t1 = datetime.strptime(d['createTime'], '%Y-%m-%dT%H:%M:%S')
    ts = datetime.strptime('2018-07-09T15:00:08', '%Y-%m-%dT%H:%M:%S')
    if t1 > ts:
        process(0)
    else:
        process(1)

file_object.close()  

for index in validDate:
    validDate[index] = str(validDate[index])

file_object = open('validUntil.txt', 'w',encoding='utf-8')
file_object.write(str(validDate))
file_object.close()  
print(validDate)