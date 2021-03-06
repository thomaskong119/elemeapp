# coding=utf-8
import json
import math
import time
import urllib.request
import urllib.response
from datetime import datetime, timedelta
from pprint import pprint

import schedule

ordertemp = [0] * 50
orderlast = [0] * 50
dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
urlcomment = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=GadgetzanAPIService.getAppraisalListByServiceNO'
orderurl = 'https://app-api.shop.ele.me/buttonwood/invoke/?method=ClassifyService.getServicesByClassifyCode'
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
global ksid
test = 1


def updateksid():
    global ksid
    file_temp = open('ksid.txt', 'r')
    ksid = file_temp.readline()
    # ksid = "MTUwMDFiZGMtNjVkNC00NmY01fXI9pYmNlMW"
    return ksid


# 实时抓取评价


def jobgetcomment():

    try:
        file_temp = open('getcomment.txt', 'r')
        file_temp.close()
    except:
        pass

    file_object = open('getcomment.txt', 'a')
    sent = 0
    content = ""

    for service in [xpgid, newxpgid, chainxpgid, sqid]:
        if service == xpgid:
            tempname = xpgname
        elif service == newxpgid:
            tempname = newxpgname
        elif service == chainxpgid:
            tempname = chainxpgname
        elif service == sqid:
            tempname = sqname

        data = {
            "id": "2C0DE4DBA2E8400DBCCF8AE4F779CCF2|1526630263938",
            "metas": {
                "appName": "melody",
                "appVersion": "4.4.0",
                "ksid": ksid,
                "key": "1.0.0",
            },
            "ncp": "2.0.0",
            "service": "GadgetzanAPIService",
            "method": "getAppraisalListByServiceNO",
            "params": {"offset": 0, "limit": 5, "serviceNO": service},
        }

        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(urlcomment, data=params, headers=header)
        try:
            res = urllib.request.urlopen(req)
            d1 = json.load(res)
            d1 = d1['result']['result']
        except IOError:
            file_object.write("\nError\n")
            print("Error, will try again")
            jobgetcomment()
        except TypeError:
            content = '被饿了么反爬了，请更新ksid'
        else:
            for index in range(len(d1)):
                try:
                    if datetime.now() - timedelta(minutes=10) > datetime.strptime(
                        d1[index]['createTime'], '%Y-%m-%d %H:%M:%S'
                    ):
                        print(tempname + "Nothing New --getcomment")
                    elif int(d1[index]['compositionalScore']) < 5:
                        file_object.write(
                            "\n"
                            + tempname
                            + " "
                            + str(d1[index]['orderNO'])
                            + " "
                            + str(d1[index]['compositionalScore'])
                            + str(d1[index]['valuator'])
                            + str(d1[index]['createTime'])
                            + "\n"
                        )
                        content += (
                            tempname
                            + " "
                            + str(d1[index]['createTime'])
                            + "有新的差评，"
                            + str(d1[index]['compositionalScore'])
                            + "分来自于"
                            + str(d1[index]['valuator'])
                            + "用户说"
                            + str(d1[index]['content'] + "\n")
                        )
                        print("New Comment" + "\n--getcomment")
                        sent = 1
                except TypeError:
                    pass

    file_object.write(
        str(datetime.now()) + "\n==========================================="
    )
    file_object.close()

    mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": [mobilelist], "isAtAll": False},
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers=header)

    if test == 0:
        if sent == 1:
            dingres = urllib.request.urlopen(dingreq)
            print(str(dingres.read()) + "\nSent --getcomment")
            sent = 0
    elif sent == 1:
        print("Test\nSent --getcomment")
        sent = 0


# 评分计算


def jobgetallcomment():

    content = ""
    file_object = open('getallcomment.txt', 'w')

    res = query("xpg")
    # print ("\n小评果"+res[0])
    file_object.write("\n小评果" + res[2])
    content += "\n小评果" + res[0]

    res = query("dkd")
    # print ("\n店客多"+res[0])
    file_object.write("\n店客多" + res[2])
    content += "\n店客多" + res[0]

    res = query("cjdz")
    # print ("\n超级店长"+res[0])
    file_object.write("\n超级店长" + res[2])
    content += "\n超级店长" + res[0]

    file_object.write(
        "\n" + str(datetime.now()) + "\n==========================================="
    )
    file_object.close()
    print(str(datetime.now()))

    mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": [mobilelist], "isAtAll": False},
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers=header)
    if test == 0:
        dingres = urllib.request.urlopen(dingreq)
        print(str(dingres.read()) + "\n评分计算完成，发送成功")
    else:
        print(content)
        print("评分计算完成，发送成功（测试）")


def query(request):

    if request == "dkd":
        tempid = dkdid
    elif request == "cjdz":
        tempid = cjdzid
    elif request == "xpg":
        tempid = xpgid
    elif request == "cjjp":
        tempid = cjjpid

    offset = 0
    limit = 200
    count = 0
    scoresum = 0
    remain = 0
    filetext = ""
    antispyder = 0

    while True:
        data = {
            "id": "008DBE4D482D431BBAC8ECC11E7EABE4|1528683444787",
            "metas": {
                "appName": "melody",
                "appVersion": "4.4.0",
                "ksid": ksid,
                "key": "1.0.0",
            },
            "ncp": "2.0.0",
            "service": "GadgetzanAPIService",
            "method": "getAppraisalListByServiceNO",
            "params": {"offset": offset, "limit": limit, "serviceNO": tempid},
        }
        params = json.dumps(data).encode('utf8')
        req = urllib.request.Request(urlcomment, data=params, headers=header)
        try:
            res = urllib.request.urlopen(req)
            d1 = json.load(res)
            if d1['result']['result'] == None:
                break
            try:
                if d1['error']['code'] == 'SERVER_ERROR':
                    print("ServerError, will try again")
                    jobgetallcomment()
            except:
                pass
        except TypeError:
            content = '被饿了么反爬了，请更新ksid'
            antispyder = 1
            break
        else:
            d1 = d1['result']['result']
            for index in range(len(d1)):
                t1 = datetime.strptime(d1[index]['createTime'], '%Y-%m-%d %H:%M:%S')
                d = datetime.now() - timedelta(days=900)
                if t1 > d:
                    if (
                        ("i**1" in d1[index]['valuator'])
                        | ("i**2" in d1[index]['valuator'])
                        | ("i**v" in d1[index]['valuator'])
                    ):
                        filetext += (
                            "\n"
                            + str(d1[index]['orderNO'])
                            + " "
                            + str(d1[index]['compositionalScore'])
                            + " "
                            + str(d1[index]['createTime'])
                        )
                        count += 1
                        scoresum += int(d1[index]['compositionalScore'])
                        # pass
                    else:
                        filetext += (
                            "\n"
                            + str(d1[index]['orderNO'])
                            + " "
                            + str(d1[index]['compositionalScore'])
                            + " "
                            + str(d1[index]['createTime'])
                        )
                        count += 1
                        scoresum += int(d1[index]['compositionalScore'])
                else:
                    break

            offset += limit

    # print(count)
    if antispyder == 0:
        scorenow = (round_up(scoresum / count * 10000)) / 10000
        content = "目前总共" + str(count) + "条评价\n评分：" + str(scorenow) + "\n"
        for score in range(math.ceil(scoresum / count * 10), 51, 1):
            while round_up(scoresum / count) * 10 < score:
                scoresum += 5.0
                count += 1
                remain += 1
            content += "距离" + str(score / 10) + "分还差" + str(remain) + "条好评" + "\n"
    else:
        print(content)
        pass
    return content, count, filetext


# 销量统计


def jobsendPostDing():

    data = {
        "id": "E8EA1587AC8040F29AF64EC30294E399|1528683065007",
        "metas": {
            "appName": "melody",
            "appVersion": "4.4.0",
            "ksid": ksid,
            "key": "1.0.0",
        },
        "ncp": "2.0.0",
        "service": "ClassifyService",
        "method": "getServicesByClassifyCode",
        "params": {"classifyCode": "1", "offset": 0, "limit": 99},
    }

    file_object = open('ordercount.txt', 'a')

    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(orderurl, data=params, headers=header)
    res = urllib.request.urlopen(req)

    d1 = json.load(res)
    # print(d1)
    try:
        d1 = d1['result']['result']
        content = ''
        for index in range(len(d1)):
            ordertemp[index] = int(d1[index]['orderCount']) - orderlast[index]
            orderlast[index] = int(d1[index]['orderCount'])
            content += (
                str(d1[index]['serviceName'])
                + str(d1[index]['orderCount'])
                + "/"
                + str(ordertemp[index])
                + "\n"
            )
            file_object.write(
                str(d1[index]['serviceName'])
                + str(d1[index]['orderCount'])
                + "/"
                + str(ordertemp[index])
                + "\n"
            )
    except TypeError:
        content = '被饿了么反爬了，请更新ksid'

    file_object.write(
        str(datetime.now()) + "\n===========================================\n"
    )
    file_object.close()

    mobilelist = "18513249383"
    dingdata = {
        "msgtype": "text",
        "text": {"content": content + str(datetime.now())},
        "at": {"atMobiles": [mobilelist], "isAtAll": False},
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers=header)

    # appid = '22547'
    # to = '18511067574'
    # signature = 'dded839a7db21a859155793987c46c85'
    # submaildata = 'appid='+appid+'&to='+to+'&content=【小评果】'+content+'退订回N &signature='+signature
    # submailurl = 'https://api.mysubmail.com/message/send.json'
    # submailparam = submaildata.encode('utf8')
    # subreq = urllib.request.Request(submailurl, data=submailparam)
    if int(datetime.now().hour) in range(0, 8):
        print(str(datetime.now().hour) + " Pass" + "\n销量统计完成，不发送")
    elif test == 0:
        # subres = urllib.request.urlopen(subreq)
        # d2 = json.load(subres)
        dingres = urllib.request.urlopen(dingreq)
        print(str(dingres.read()) + "\n销量统计完成，发送成功")
    else:
        print("销量统计完成，发送成功（测试）")


# 四舍五入，小数点后一位


def round_up(value):
    return round(value * 10) / 10.0


updateksid()
jobsendPostDing()
jobgetcomment()
jobgetallcomment()

# 定时任务
schedule.every().day.at("10:00").do(jobgetallcomment)
schedule.every(10).minutes.do(updateksid)
schedule.every(10).minutes.do(jobgetcomment)
for runtime in range(8, 24):
    schedule.every().day.at(str(runtime) + ":59").do(jobsendPostDing)

while True:
    schedule.run_pending()
    time.sleep(1)
