# -*- coding: utf-8 -*- 
import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule
import math

# 店客多  749ff8fc717c4426e825e8d42ac6d4ce
# 超级店长  7c1fccc89fd9c3a356ab276fdf9e4403
# 小评果  6d4fdd6db6c4c2a0507599e5c29efdfb
# 超级竞品 4cef596097ddf479b2cc16b0df3aedf2
dkdid = "749ff8fc717c4426e825e8d42ac6d4ce"
cjdzid = "7c1fccc89fd9c3a356ab276fdf9e4403"
xpgid = "6d4fdd6db6c4c2a0507599e5c29efdfb"
cjjpid = "4cef596097ddf479b2cc16b0df3aedf2"
    
url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
header = {'Content-Type': 'application/json'}

def job():

    file_object = open('getallcomment.txt', 'w') 

    res = query("xpg")
    print ("\n小评果"+res[0])
    file_object.write("\n小评果"+res[2])

    res = query("dkd")
    print ("\n店客多"+res[0])
    file_object.write("\n店客多"+res[2])

    res = query("cjdz")
    print ("\n超级店长"+res[0])
    file_object.write("\n超级店长"+res[2])

    file_object.write("\n" + str(datetime.now())+"\n===========================================")
    file_object.close()
    print (str(datetime.now()))

    # mobilelist = "18600536524"
    # dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
    # dingdata = {
    #     "msgtype": "text",
    #     "text": {
    #         "content": content
    #     },
    #     "at": {
    #         "atMobiles": [
    #             mobilelist
    #         ],
    #         "isAtAll": False
    #     }
    # }
    # json_str = json.dumps(dingdata).encode('utf8')
    # dingreq = urllib.request.Request(dingurl, data=json_str, headers= header)
    # dingres = urllib.request.urlopen(dingreq)
    # print (dingres.read())

def query(request):

    if request == "dkd":
        tempid = dkdid
    elif request == "cjdz":
        tempid = cjdzid
    elif request == "xpg":
        tempid = xpgid
    elif request == "cjjp":
        tempid = cjjpid
    
    offset = 0
    limit = 200
    count = 0
    scoresum = 0
    remain = 0
    filetext = ""
    score = {}

    data = {"id":"008DBE4D482D431BBAC8ECC11E7EABE4|1528683444787","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"NGU3ZTI1YTItODJlZS00NDEw1fWK8KNmJkMG","key":"1.0.0"},"ncp":"2.0.0","service":"GadgetzanAPIService","method":"getAppraisalListByServiceNO","params":{"offset":offset,"limit":limit,"serviceNO":tempid}}
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)

    while True:
        data = {"id": "008DBE4D482D431BBAC8ECC11E7EABE4|1528683444787", "metas": {"appName": "melody", "appVersion": "4.4.0", "ksid": "NGU3ZTI1YTItODJlZS00NDEw1fWK8KNmJkMG",
                                                                                "key": "1.0.0"}, "ncp": "2.0.0", "service": "GadgetzanAPIService", "method": "getAppraisalListByServiceNO", "params": {"offset": offset, "limit": limit, "serviceNO": tempid}}
        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(url, data=params, headers=header)
        res = urllib.request.urlopen(req)
        d1 = json.load(res)
        if d1['result']['result'] == None:
            break
        try:
            if d1['error']['code'] == 'SERVER_ERROR':
                print("ServerError, will try again")
                job()
        except:
            pass

        d1 = d1['result']['result']

        for index in range(len(d1)):
            t1 = datetime.strptime(
                d1[index]['createTime'], '%Y-%m-%d %H:%M:%S')
            d = datetime.now() - timedelta(days=30)
            if t1 > d:
                # score[]
                filetext += "\n" + str(d1[index]['orderNO']) + " " + str(
                    d1[index]['compositionalScore'])+" " + str(d1[index]['createTime'])
                count += 1
                scoresum += int(d1[index]['compositionalScore'])
            else:
                break

        offset += limit

    # print(count)
    scorenow = (round_up(scoresum / count*10000))/10000
    content = "目前总共" + str(count) +"条评价\n评分：" + str(scorenow) + "\n"
    for score in range(math.ceil(scoresum / count*10), 51, 1):
        while round_up(scoresum / count)*10 < score:
            scoresum += 5.0
            count += 1
            remain += 1
        content += "距离" + str(score/10) + "分还差" + \
            str(remain) + "条好评" + "\n"
    return content, count, filetext

def round_up(value):     
      return round(value * 10) / 10.0

job()
for runtime in range(8,24):
    schedule.every().day.at(str(runtime)+":59").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
