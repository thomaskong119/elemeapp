import urllib.request
import json
from pprint import pprint
from datetime import datetime
import time
import schedule

ordertemp = [0]*20
orderlast = [0]*20
dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
urlcomment = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
header = {'Content-Type': 'application/json'}

def jobgetcomment():

    with open('commentbody.json') as f:
        data = json.load(f)
    
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

def jobgetallcomment():

    with open('comment.json') as f:
        data = json.load(f)
    
    url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
    header = {'Content-Type': 'application/json'}

    file_object = open('commentdetail.txt', 'a') 

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']

    print (d1[0])

    for index in range(len(d1)):
        file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore']))

    file_object.write(str(datetime.now())+"\n===========================================")
    file_object.close()

def jobsendPostDing():

    with open('body.json') as f:
        data = json.load(f)

    file_object = open('ordercount.txt', 'a') 

    url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=ClassifyService.getServicesByClassifyCode'
    header = {'Content-Type': 'application/json'}

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
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

    dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
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

jobsendPostDing()
jobgetcomment()
jobgetallcomment()
schedule.every(1).hour.do(jobsendPostDing)
schedule.every().day.do(jobgetallcomment)
schedule.every(0.2).minutes.do(jobgetcomment)

while True:
    schedule.run_pending()
    time.sleep(1)
