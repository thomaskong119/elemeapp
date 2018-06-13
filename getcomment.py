
import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule

dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
urlcomment = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
header = {'Content-Type': 'application/json'}
newxpgid = "266c3696a385377e647a9ac28f2bc1db"
chainxpgid = "52f0b0f2bd8b19061654ba10608ab17a"
sqid = "3cd8c323d6f4e2baa6107158802b49bb"
dkdid = "749ff8fc717c4426e825e8d42ac6d4ce"
cjdzid = "7c1fccc89fd9c3a356ab276fdf9e4403"
xpgid = "6d4fdd6db6c4c2a0507599e5c29efdfb"
cjjpid = "4cef596097ddf479b2cc16b0df3aedf2"
newxpgname = "小评果新店版"
chainxpgname = "小评果连锁版"
xpgname = "小评果正式版"
sqname = "商圈排名"
test = 1

def jobgetcomment():

    try:
        file_temp = open('getcomment.txt','r')
        file_temp.close()
    except:
        pass

    file_object = open('getcomment.txt', 'a') 
    sent = 0
    content = ""

    for service in [xpgid,newxpgid,chainxpgid,sqid]:
    # for service in [newxpgid,xpgid]:
        if service == xpgid:
            tempname = xpgname
        elif service == newxpgid:
            tempname = newxpgname
        elif service == chainxpgid:
            tempname = chainxpgname
        elif service == sqid:
            tempname = sqname

        data = {"id":"2C0DE4DBA2E8400DBCCF8AE4F779CCF2|1526630263938","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"ZTliYTJiMDgtOGQ5NC00NWZk1fJYcQYWZlOT","key":"1.0.0"},"ncp":"2.0.0","service":"GadgetzanAPIService","method":"getAppraisalListByServiceNO","params":{"offset":0,"limit":5,"serviceNO":service}}

        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(urlcomment, data=params, headers=header)
        try:
            res = urllib.request.urlopen(req)
            d1 = json.load(res)
            d1 = d1['result']['result']
        except IOError:
            file_object.write("\nError\n")
            print ("Error, will try again")
            jobgetcomment()
        except TypeError:
            pass
        else:
            for index in range(5):
                if datetime.now() - timedelta(minutes=10) > datetime.strptime(d1[index]['createTime'], '%Y-%m-%d %H:%M:%S'):
                    pass
                elif int(d1[index]['compositionalScore']) < 5:
                    file_object.write("\n" + tempname + " " + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore'])+ str(d1[index]['valuator']) + str(d1[index]['createTime']) +"\n")
                    content += tempname + " " +str(d1[index]['createTime'])+"有新的差评，"+str(d1[index]['compositionalScore'])+"分来自于"+str(d1[index]['valuator'])+"用户说"+str(d1[index]['content'])
                    print ("New Comment" + "\n--getcomment")
                    sent = 1

    file_object.write(str(datetime.now())+"\n===========================================")
    file_object.close()

    mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": content
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

    if test == 0:
        if int(d1[0]['compositionalScore']) == 5.0:
            pass
        elif sent == 1:
            dingres = urllib.request.urlopen(dingreq)
            print (str(dingres.read()) + "\nSent --getcomment")
            sent = 0
    elif sent == 1:
        print ("Test\nSent --getcomment")
        sent = 0

jobgetcomment()
schedule.every(10).minutes.do(jobgetcomment)

while True:
    schedule.run_pending()
    time.sleep(1)
