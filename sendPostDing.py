import urllib.request
import json
from pprint import pprint
from datetime import datetime
import time
import schedule

ordertemp = [0]*20
orderlast = [0]*20

def job():

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

    # print (content)

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
        print (str(datetime.now().hour)+" Pass")
    else:
        subres = urllib.request.urlopen(subreq)
        d2 = json.load(subres)
        dingres = urllib.request.urlopen(dingreq)
        print (d2)
        print (dingres.read())
        pass

job()
# schedule.every(0.1).minutes.do(job)
schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.01)
