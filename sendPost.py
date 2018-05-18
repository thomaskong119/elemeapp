import urllib.request
import json
from pprint import pprint
from datetime import datetime
import time
import schedule

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
        # print(d1[index]['serviceName'] + str(d1[index]['orderCount']))
        content += (d1[index]['serviceName'] + str(d1[index]['orderCount'])+"\n")
        file_object.write(d1[index]['serviceName'] + str(d1[index]['orderCount'])+"\n")

    file_object.write(str(datetime.now()))
    file_object.close()

    # print (content)

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
        print (d2)

job()
schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)