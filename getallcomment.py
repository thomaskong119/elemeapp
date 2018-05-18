import urllib.request
import json
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import time
import schedule

def job():

    with open('comment.json') as f:
        data = json.load(f)
    
    url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
    header = {'Content-Type': 'application/json'}

    file_object = open('commentdetail.txt', 'w') 

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    d1 = d1['result']['result']

    # for index in range(len(d1)):
    #     file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore']))
    count = 0
    
    for index in range(len(d1)):
        t1 = datetime.strptime(d1[index]['createTime'], '%Y-%m-%d %H:%M:%S')
        d = datetime.now() - timedelta(days=30)
        if t1 > d:
            file_object.write("\n" + str(d1[index]['orderNO']) +" "+ str(d1[index]['compositionalScore']))
            count += 1
        else:
            break

    print (count)
    file_object.write(str(datetime.now())+"\n===========================================")
    file_object.close()

job()
# schedule.every(0.2).minutes.do(job)
schedule.every(1).hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(0.01)
