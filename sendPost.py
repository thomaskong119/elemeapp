import urllib.request
import json
from pprint import pprint
from time import strftime,gmtime
from submail import submail

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

for index in range(len(d1)):
    print(d1[index]['serviceName'] + str(d1[index]['orderCount']))
    file_object.write(d1[index]['serviceName'] + str(d1[index]['orderCount'])+"\n")

file_object.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n=======================================")

file_object.close()

manager = submail.build("sms")
msg = manager.message()
msg['appid'] = '22547'
msg['signature'] = 'dded839a7db21a859155793987c46c85'
msg['to'] = '18676559554'
# variables in your message template
msg['vars'] = {"var1":"xxxxx","var2":"yyyy"}
# send message,return response
result = msg.send(stype="xsend", inter=False)

if(res.status != 200):
    exit()
