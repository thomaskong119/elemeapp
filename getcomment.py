import urllib.request
import json
from pprint import pprint
from datetime import datetime
import time
import schedule

def job():

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

    url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
    header = {'Content-Type': 'application/json'}

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']
    sent = 0

    if str(targetLine[0:17]) != str(d1[0]['orderNO']):
        for index in range(len(d1)):
            file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore'])+ str(d1[index]['valuator']) + str(d1[index]['createTime']) +"\n")
        print ("New Comment")
        sent = 1
    else:
        file_object.write("\n"+ str(d1[0]['orderNO']) + "Not New\n")
        print ("Nothing New")
    file_object.write(str(datetime.now())+"\n===========================================")
    file_object.close()

    dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
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
        print (dingres.read())
        sent = 0


job()
schedule.every(0.2).minutes.do(job)
# schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.01)
