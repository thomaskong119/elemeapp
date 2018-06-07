import urllib.request
import json
from datetime import datetime
import schedule
import time

ordertemp = [0]*20
orderlast = [0]*20
dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
orderurl = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=ClassifyService.getServicesByClassifyCode'
header = {'Content-Type': 'application/json'}
test = 1

def jobsendPostDing():

    data = {"id":"5DF959EFBA4B45B9936F604665A92916|1525949952348","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"NjhhOTRjN2YtYTQwMC00MDE01fGeCEZjBiYz","key":"1.0.0"},"ncp":"2.0.0","service":"ClassifyService","method":"getServicesByClassifyCode","params":{"classifyCode":"1","offset":0,"limit":99}}

    file_object = open('ordercount.txt', 'a') 
    
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(orderurl, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']

    print (d1)

    content = ''

    for index in range(len(d1)):
        ordertemp[index] = int(d1[index]['orderCount']) - orderlast[index]
        orderlast[index] = int(d1[index]['orderCount'])
        content += (str(d1[index]['serviceName']) + str(d1[index]['orderCount'])+ "/" +str(ordertemp[index]) + "\n")
        file_object.write(str(d1[index]['serviceNo']) + str(d1[index]['serviceName']) + str(d1[index]['orderCount']) + "/" +str(ordertemp[index]) + "\n")

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

    # appid = '22547'
    # to = '18511067574'
    # signature = 'dded839a7db21a859155793987c46c85'
    # submaildata = 'appid='+appid+'&to='+to+'&content=【小评果】'+content+'退订回N &signature='+signature
    # submailurl = 'https://api.mysubmail.com/message/send.json'
    # submailparam = submaildata.encode('utf8')
    # subreq = urllib.request.Request(submailurl, data=submailparam)
    if int(datetime.now().hour) in range(0,8):
        print (str(datetime.now().hour)+" Pass" + "\n--sendPostDing")
    elif test ==0:
        # subres = urllib.request.urlopen(subreq)
        # d2 = json.load(subres)
        dingres = urllib.request.urlopen(dingreq)
        print (str(dingres.read()) + "\n--sendPostDing")
    else:
        print ("sendPostDing test")

# 四舍五入，小数点后一位
def round_up(value):     
      return round(value * 10) / 10.0

jobsendPostDing()

# 定时任务
for runtime in range(8,24):
    schedule.every().day.at(str(runtime)+":59").do(jobsendPostDing)

while True:
    schedule.run_pending()
    time.sleep(1)