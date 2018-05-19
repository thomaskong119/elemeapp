import urllib.request
import json
from pprint import pprint
from datetime import datetime
import time
import schedule
import math

ordertemp = [0]*20
orderlast = [0]*20
dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
urlcomment = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
orderurl = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=ClassifyService.getServicesByClassifyCode'
header = {'Content-Type': 'application/json'}

# 实时抓取评价
def jobgetcomment():

    data = {"id":"2C0DE4DBA2E8400DBCCF8AE4F779CCF2|1526630263938","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"ZTliYTJiMDgtOGQ5NC00NWZk1fJYcQYWZlOT","key":"1.0.0"},"ncp":"2.0.0","service":"GadgetzanAPIService","method":"getAppraisalListByServiceNO","params":{"offset":0,"limit":1,"serviceNO":"6d4fdd6db6c4c2a0507599e5c29efdfb"}}
    
    targetLine = ""

    try:
        file_temp = open('commentdetail.txt','r')
        mLines = file_temp.readlines()
        targetLine = mLines[-3]
        file_temp.close()
    except FileNotFoundError:
        pass

    file_object = open('commentdetail.txt', 'a') 

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(urlcomment, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']
    sent = 0

    if str(targetLine[0:17]) != str(d1[0]['orderNO']):
        for index in range(len(d1)):
            file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore'])+ str(d1[index]['valuator']) + str(d1[index]['createTime']) +"\n")
        print ("New Comment" + "\n--getcomment")
        sent = 1
    else:
        file_object.write("\n"+ str(d1[0]['orderNO']) + "Not New\n")
        print ("Nothing New" + "\n--getcomment")
    file_object.write(str(datetime.now())+"\n===========================================")
    file_object.close()

    mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": str(d1[0]['createTime'])+"有新的差评，"+str(d1[0]['compositionalScore'])+"分来自于"+str(d1[0]['valuator'])+"用户说"+str(d1[0]['content'])
        },
        "at": {
            "atMobiles": [
                mobilelist
            ],
            "isAtAll": False
        }
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers= header)

    if int(d1[0]['compositionalScore']) == 5.0:
        pass
    elif sent == 1:
        dingres = urllib.request.urlopen(dingreq)
        print (dingres.read() + "\n--getcomment")
        sent = 0

# 评分计算
def jobgetallcomment():

    data = {"id":"2C0DE4DBA2E8400DBCCF8AE4F779CCF2|1526630263938","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"NjhhOTRjN2YtYTQwMC00MDE01fGeCEZjBiYz","key":"1.0.0"},"ncp":"2.0.0","service":"GadgetzanAPIService","method":"getAppraisalListByServiceNO","params":{"offset":0,"limit":500,"serviceNO":"6d4fdd6db6c4c2a0507599e5c29efdfb"}}
    
    file_object = open('commentdetail.txt', 'w') 

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(urlcomment, data=params, headers=header)
    try:
        res = urllib.request.urlopen(req)
        d1 = json.load(res)
        d1 = d1['result']['result']

        count = 0
        scoresum = 0
        remain = 0
        
        for index in range(len(d1)):
            t1 = datetime.strptime(d1[index]['createTime'], '%Y-%m-%d %H:%M:%S')
            d = datetime.now() - timedelta(days=30)
            if t1 > d:
                file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore'])+" "+ str(d1[index]['createTime']))
                count += 1
                scoresum += int(d1[index]['compositionalScore'])
            else:
                break

        scorenow = (round_up(scoresum / count*10000))/10000
        content = "目前评分：" + str(scorenow) + "\n"
        for score in range(math.ceil(scoresum / count*10), 51, 1):
            while round_up(scoresum / count)*10 < score:
                scoresum += 5.0
                count += 1
                remain += 1
            content += "距离" + str(score/10) + "分还差" + str(remain) + "条好评" + "\n"

        print (content)
    except urllib.error.HTTPError:
        print ("HTTPError, will try again")
        file_object.write("HTTPError")
        jobgetallcomment()

    file_object.write("\n" + str(datetime.now())+"\n===========================================")
    file_object.close()

    mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": str(d1[0]['createTime'])+"有新的差评，"+str(d1[0]['compositionalScore'])+"分来自于"+str(d1[0]['valuator'])+"用户说"+str(d1[0]['content'])
        },
        "at": {
            "atMobiles": [
                mobilelist
            ],
            "isAtAll": False
        }
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers= header)
    dingres = urllib.request.urlopen(dingreq)
    print (dingres.read() + "\n--getallcomment")

# 销量统计
def jobsendPostDing():

    data = {"id":"5DF959EFBA4B45B9936F604665A92916|1525949952348","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"NjhhOTRjN2YtYTQwMC00MDE01fGeCEZjBiYz","key":"1.0.0"},"ncp":"2.0.0","service":"ClassifyService","method":"getServicesByClassifyCode","params":{"classifyCode":"1","offset":0,"limit":99}}

    file_object = open('ordercount.txt', 'a') 
    
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(orderurl, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']

    content = ''

    for index in range(len(d1)):
        ordertemp[index] = int(d1[index]['orderCount']) - orderlast[index]
        orderlast[index] = int(d1[index]['orderCount'])
        content += (d1[index]['serviceName'] + str(d1[index]['orderCount'])+ "/" +str(ordertemp[index]) + "\n")
        file_object.write(d1[index]['serviceName'] + str(d1[index]['orderCount']) + "/" +str(ordertemp[index]) + "\n")

    file_object.write(str(datetime.now())+"\n===========================================\n")
    file_object.close()

    mobilelist = "18513249383"
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": content+str(datetime.now())
        },
        "at": {
            "atMobiles": [
                mobilelist
            ],
            "isAtAll": False
        }
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers= header)

    appid = '22547'
    to = '18511067574'
    signature = 'dded839a7db21a859155793987c46c85'
    submaildata = 'appid='+appid+'&to='+to+'&content=【小评果】'+content+'退订回N &signature='+signature
    submailurl = 'https://api.mysubmail.com/message/send.json'
    submailparam = submaildata.encode('utf8')
    subreq = urllib.request.Request(submailurl, data=submailparam)
    if int(datetime.now().hour) in range(0,8):
        print (str(datetime.now().hour)+" Pass" + "\n--sendPostDing")
    else:
        subres = urllib.request.urlopen(subreq)
        d2 = json.load(subres)
        dingres = urllib.request.urlopen(dingreq)
        print (d2 + "\n--sendPostDing")
        print (dingres.read())
        pass

# 四舍五入，小数点后一位
def round_up(value):     
      return round(value * 10) / 10.0

jobsendPostDing()
jobgetcomment()
jobgetallcomment()

# 定时任务
schedule.every().day.at("10:00").do(jobgetallcomment)
schedule.every(0.2).minutes.do(jobgetcomment)
for runtime in range(8,24):
    schedule.every().day.at(str(runtime)+":59").do(jobsendPostDing)

while True:
    schedule.run_pending()
    time.sleep(1)
