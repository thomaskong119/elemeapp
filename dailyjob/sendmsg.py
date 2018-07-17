# -*- coding: utf-8 -*-
import urllib.request
import json
from datetime import datetime
from datetime import timedelta

header = {'Content-Type': 'application/json'}

def sendmsg(to, content):
    appid = '24407'
    to = to
    content = content
    print(content)
    signature = 'ce61d45e3936c3645297213cde56f536'
    submaildata = 'appid='+appid+'&to='+to + \
        '&content=【小评果】'+content+'退订回N &signature='+signature
    submailurl = 'https://api.mysubmail.com/message/send.json'
    submailparam = submaildata.encode('utf8')
    subreq = urllib.request.Request(submailurl, data=submailparam)
    subres = urllib.request.urlopen(subreq)
    d2 = json.load(subres)
    print(d2)

def sendding(url, to, content):
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": content+str(datetime.now())
        },
        "at": {
            "atMobiles": [
                to
            ],
            "isAtAll": False
        }
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(url, data=json_str, headers=header)
    dingres = urllib.request.urlopen(dingreq)
    print(content)
    print(str(dingres.read()))