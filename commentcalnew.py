# -*- coding: utf-8 -*-
import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule
import math

url = 'https://open.shop.ele.me/api/invoke?method=GadgetzanAPIService.getAppraisalListByAppId'
header = {'Content-Type': 'application/json'}


def job(request):
    file_object = open('commentcalnew.txt', 'w')

    appid = request

    offset = 0
    limit = 500
    count = 0
    scoresum = 0
    remain = 0
    filetext = ""
    _temp = []
    score = {}
    counter = {}
    flag = 1

    while flag:
        data = {"id": "488aa0de-1a25-4654-ab2c-895aaebeccd4", "method": "getAppraisalListByAppId", "service": "GadgetzanAPIService", "params": {"condition": {"appId": appid,
                                                                                                                                                              "offset": offset, "limit": limit, "sourceEnum": "APPID"}}, "metas": {"appName": "Odin", "appVersion": "4.4.0", "ksid": "ZTdlMmY3ZGEtYWM3NS00ODgw1fYoOmMWIwMj"}, "ncp": "2.0.0"}
        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(url, data=params, headers=header)
        res = urllib.request.urlopen(req)
        d1 = json.load(res)
        try:
            if d1['result']['result'] == None:
                break
        except TypeError:
            break

        try:
            if d1['error']['code'] == 'SERVER_ERROR':
                print("ServerError, will try again")
                job(request)
        except:
            pass

        d1 = d1['result']['result']
        for index in range(len(d1)):
            t1 = datetime.strptime(
                d1[index]['createTime'], '%Y-%m-%d %H:%M:%S')
            d = datetime.now() - timedelta(days=30)
            if t1 > d:
                if d1[index]['orderBaseView']['shopID'] in counter.keys():
                    if counter[d1[index]['orderBaseView']['shopID']] == 3:
                        print('duplicated')
                        continue
                    else:
                        counter[d1[index]['orderBaseView']['shopID']] += 1
                        scoresum += d1[index]['compositionalScore']
                        count += 1
                else:
                    counter[d1[index]['orderBaseView']['shopID']] = 1
                    scoresum += d1[index]['compositionalScore']
                    count += 1
                filetext += "\n" + str(d1[index]['orderNO']) + " " + str(
                    d1[index]['compositionalScore'])+" " + str(d1[index]['createTime']) + " " + str(d1[index]['orderBaseView']['shopID'])
            else:
                flag = 0
        offset += limit

    # print(filetext)
    # print(count)
    # print(score)
    # print(counter)
    file_object.write(filetext)
    file_object.close()
    # print(str(datetime.now()))
    # print(appid)
    scorenow = (round_up(scoresum / count*10000))/10000
    content = "目前总共" + str(count) + "条评价\n评分：" + str(scorenow) + "\n"
    for score in range(math.ceil(scoresum / count*10), 51, 1):
        while round_up(scoresum / count)*10 < score:
            scoresum += 5.0
            count += 1
            remain += 1
        content += "距离" + str(score/10) + "分还差" + \
            str(remain) + "条好评" + "\n"
    print(content)


def round_up(value):
    return round(value * 10) / 10.0


job('79237657')
# job('72863852')
