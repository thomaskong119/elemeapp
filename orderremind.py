import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule
import math

dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
url = 'https://open.shop.ele.me/api/invoke?method=GadgetzanAPIService.mgetOrders'
header = {'Content-Type': 'application/json'}
msgcontent = '感谢您支持小评果，订购完成后软件需要您登陆设置才能正常工作哦~赶快打开商家版APP-服务市场-我的服务-找到小评果开启口碑评分提升之旅吧！有问题请及时联系客服18701526781'


def job(request):

    appid = request

    try:
        file_temp = open('orderremind.txt', 'r')
        file_temp.close()
    except:
        pass

    file_object = open('orderremind.txt', 'a')
    content = ""
    filetext = ""

    data = {"id": "a3611e87-2c3d-48c1-b1bf-f10bfb9c8667", "method": "mgetOrders", "service": "GadgetzanAPIService", "params": {"condition": {"appId": appid, "orderNO": None, "orderStatus": "ALL",
                                                                                                                                             "beginTime": None, "endTime": None, "offset": 0, "limit": 50, "source": "APPID"}}, "metas": {"appName": "Odin", "appVersion": "4.4.0", "ksid": "ZTdlMmY3ZGEtYWM3NS00ODgw1fYoOmMWIwMj"}, "ncp": "2.0.0"}
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
    try:
        res = urllib.request.urlopen(req)
        d1 = json.load(res)
        d1 = d1['result']['result']
    except IOError:
        file_object.write("\nError\n")
        print("Error, will try again")
        job(appid)
    except TypeError:
        content = '被饿了么反爬了，请更新ksid'
    else:
        for index in range(len(d1)):
            try:
                if datetime.now() - timedelta(minutes=10) > datetime.strptime(d1[index]['payTime'], '%Y-%m-%dT%H:%M:%S'):
                    # print(appid + " Not new order")
                    pass
                elif d1[index]['orderStatus'] == 'PAY_SUCCESS':
                    filetext += "\n" + appid + ' ' + str(d1[index]['orderNO']) + " " + str(
                        d1[index]['orderType'])+" " + str(d1[index]['payTime']) + " " + str(d1[index]['shopID']) + " " + str(d1[index]['contacts'])
                    content += "\n" + appid + ' ' + str(d1[index]['orderNO']) + " " + str(
                        d1[index]['orderType'])+" " + str(d1[index]['payTime']) + " " + str(d1[index]['shopID']) + " " + str(d1[index]['contacts'])
                    print(int(d1[index]['contacts']))
                    sendmsg(str(d1[index]['contacts']), msgcontent)
            except TypeError:
                pass

    file_object.write(str(datetime.now()) + filetext + 
                      "\n===========================================")
    file_object.close()

    # print(content)


def sendmsg(to, content):
    appid = '22547'
    to = to
    content = content
    # print(content)
    signature = 'dded839a7db21a859155793987c46c85'
    # submaildata = 'appid='+appid+'&to='+to+'&content=【小评果】'+content+'退订回N &signature='+signature
    submaildata = 'appid='+appid+'&to='+to + \
        '&content=【饿了么-小评果】'+content+'&signature='+signature
    submailurl = 'https://api.mysubmail.com/message/send.json'
    submailparam = submaildata.encode('utf8')
    subreq = urllib.request.Request(submailurl, data=submailparam)
    subres = urllib.request.urlopen(subreq)
    d2 = json.load(subres)
    print(d2)


def run():
    job('79237657')
    # job('72863852')
    print('check')


run()

schedule.every(10).minutes.do(run)
while True:
    schedule.run_pending()
    time.sleep(1)
