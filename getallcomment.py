import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule
import math

def job():

    with open('comment.json') as f:
        data = json.load(f)
    
    url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
    header = {'Content-Type': 'application/json'}

    file_object = open('commentdetail.txt', 'w') 

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
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
        job()

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

def round_up(value):     
      return round(value * 10) / 10.0

job()
for runtime in range(8,24):
    schedule.every().day.at(str(runtime)+":59").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
