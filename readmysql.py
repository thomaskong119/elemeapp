import urllib.request
import json

url = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
header = {'Content-Type': 'application/json'}
data = {"id":"2C0DE4DBA2E8400DBCCF8AE4F779CCF2|1526630263938","metas":{"appName":"melody","appVersion":"4.4.0","ksid":"NjhhOTRjN2YtYTQwMC00MDE01fGeCEZjBiYz","key":"1.0.0"},"ncp":"2.0.0","service":"GadgetzanAPIService","method":"getAppraisalListByServiceNO","params":{"offset":0,"limit":950,"serviceNO":"4cef596097ddf479b2cc16b0df3aedf2"}}
params = json.dumps(data).encode('utf8')
req = urllib.request.Request(url, data=params, headers=header)
res = urllib.request.urlopen(req)
d1 = json.load(res.text)
print (res.read())
# print (d1)
d1 = d1['result']['result']
# print (d1)