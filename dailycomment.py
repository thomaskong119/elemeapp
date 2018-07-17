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
    file_object = open('dailycomment.txt', 'w')

    appid = request

    offset = 0
    limit = 500
    count = 0
    filetext = ""
    _temp = []

    while True:
        data = {"id": "488aa0de-1a25-4654-ab2c-895aaebeccd4", "method": "getAppraisalListByAppId", "service": "GadgetzanAPIService", "params": {"condition": {"appId": appid,
                                                                                                                                                              "offset": offset, "limit": limit, "sourceEnum": "APPID"}}, "metas": {"appName": "Odin", "appVersion": "4.4.0", "ksid": "ZTdlMmY3ZGEtYWM3NS00ODgw1fYoOmMWIwMj"}, "ncp": "2.0.0"}
        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(url, data=params, headers=header)
        res = urllib.request.urlopen(req)
        d1 = json.load(res)
        if d1['result']['result'] == None:
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
            # d = datetime.now() - timedelta(days=2)
            te = datetime.strptime(datetime.today().strftime(
                "%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            ts = datetime.strptime((datetime.today(
            )-timedelta(days=1)).strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            if t1 > ts and t1 < te:
                filetext += "\n" + str(d1[index]['orderNO']) + " " + str(
                    d1[index]['compositionalScore'])+" " + str(d1[index]['createTime']) + " " + str(d1[index]['orderBaseView']['shopID'])
                if d1[index]['compositionalScore'] == 5.0:
                    _temp.append(d1[index]['orderBaseView']['shopID'])
                count += 1
            elif t1 < ts:
                break
        break

    # print(filetext)
    print(count)
    file_object.write(filetext)
    file_object.close()
    print(str(datetime.now()))
    print(appid)
    print(all_list(_temp))


def all_list(arr):
    result = {}
    for i in set(arr):
        result[arr.count(i)] = ''
    result = dict(sorted(result.items()))
    for i in set(arr):
        result[arr.count(i)] += str(i) + ', '
    for i in set(result.keys()):
        result[i] = result[i][:-2]
    return result


job('79237657')
job('72863852')
