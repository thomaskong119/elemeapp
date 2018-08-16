import json
import sys
import urllib.request
from datetime import datetime, timedelta

import pymysql
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

host = "rm-2zeqp0878qi2f6xlnrw.mysql.rds.aliyuncs.com"
database = "ele_message"
user = "sthgadmin"
password = "Sthg123456"
port = 3306
charset = 'utf8'

sqlcmd = "SELECT a.*,b.left_counter FROM t_ea_evaluate_revise_detial as a, t_ea_evaluate_revise as b where TO_DAYS(a.order_time) > TO_DAYS(NOW())-10 and a.shop_id = b.shop_id order by a.create_time desc;"


@csrf_exempt
def process(request):
    dbconn = pymysql.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
        charset=charset,
    )
    cursor = dbconn.cursor()
    shopid = request.POST.get('shopid')
    phone = request.POST.get('phone')
    orderid = request.POST.get('orderid')
    process = int(request.POST.get('process'))
    try:
        if process == 1:
            cursor.execute(
                "UPDATE t_ea_evaluate_revise_detial set is_revise=1 where shop_id = "
                + shopid
                + " and phones like '%"
                + phone
                + "%' and order_id ="
                + orderid
                + ";UPDATE t_ea_evaluate_revise SET left_counter = left_counter - 1 where shop_id= "
                + shopid
                + ";"
            )
            print("Shopid=" + shopid + " Phone=" + phone + " Success.")
        elif process == 2:
            cursor.execute(
                "UPDATE t_ea_evaluate_revise_detial set is_revise=2 where shop_id = "
                + shopid
                + " and phones like '%"
                + phone
                + "%' and order_id ="
                + orderid
                + ";"
            )
            print("Shopid=" + shopid + " Phone=" + phone + " Fail.")
        elif process == 3:
            cursor.execute(
                "UPDATE t_ea_evaluate_revise_detial set is_revise=1 where shop_id = "
                + shopid
                + " and phones like '%"
                + phone
                + "%' and order_id ="
                + orderid
                + ";"
            )
            print("Shopid=" + shopid + " Phone=" + phone + " Passit.")
        dbconn.commit()
    except:
        print("Process fail. Rollback.")
        dbconn.rollback()

    dbconn.close()
    cursor.close()
    return JsonResponse({'msg': 'ok'})


@csrf_exempt
def index(request):
    dbconn = pymysql.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
        charset=charset,
    )
    cursor = dbconn.cursor()
    cursor.execute(sqlcmd)
    results = cursor.fetchall()
    table = []
    for row in results:
        if row[12] == 0:
            row12 = "已提交"
        elif row[12] == 1:
            row12 = "修改成功"
        else:
            row12 = "修改失败"

        if row[6] == None:
            row6 = " "
        else:
            row6 = row[6]

        if row[7] == None:
            row7 = " "
        else:
            row7 = row[7]

        if row[11] == None:
            row11 = " "
        else:
            row11 = row[11]

        if row[20] > datetime.now() - timedelta(days=7):
            expired = False
        else:
            expired = True
        table.append(
            {
                'shopid': row[1],
                'evaluateid': row[2],
                'beforerating': row[4],
                'beforecontent': row[5],
                'afterrating': row6,
                'aftercontent': row7,
                'createtime': row[8],
                'revisetime': row[9],
                'creator': row[10],
                'reviser': row11,
                'isrevise': row12,
                'buyer': row[13],
                'phone': row[14],
                'beforetime': row[15],
                'aftertime': row[17],
                'ordertime': row[20],
                'appid': row[21],
                'orderid': row[22],
                'isrefund': row[23],
                'leftcount': row[25],
                'expired': expired,
            }
        )
    cursor.execute(
        "SELECT count(id) FROM `t_ea_evaluate_revise_detial` where is_revise=0;"
    )
    remaincount = cursor.fetchall()
    cursor.execute(
        "SELECT count(id) FROM `t_ea_evaluate_revise_detial` where is_revise=1;"
    )
    successcount = cursor.fetchall()
    cursor.execute(
        "SELECT count(id) FROM `t_ea_evaluate_revise_detial` where is_revise=2;"
    )
    failcount = cursor.fetchall()
    print(
        "Total count :"
        + str(remaincount[0][0])
        + str(successcount[0][0])
        + str(failcount[0][0])
    )

    dbconn.close()
    cursor.close()
    return render(
        request,
        'polls/index.html',
        {
            'results': table,
            'remaincount': remaincount[0][0],
            'successcount': successcount[0][0],
            'failcount': failcount[0][0],
        },
    )


@csrf_exempt
def remind(request):
    dbconn = pymysql.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
        charset=charset,
    )
    cursor = dbconn.cursor()
    shopid = request.POST.get('shopid')
    customer = request.POST.get('customer')
    phone = request.POST.get('phone')
    createtime = request.POST.get('createtime')
    shopname = request.POST.get('shopname')
    orderid = request.POST.get('orderid')
    content = (
        shopname[: int(shopname.index("<br>"))]
        + '于'
        + createtime
        + '提交的差评代改服务（来自顾客'
        + customer
        + ' '
        + phone
        + '）小评果客服已经与顾客取得联系并协商修改。最终结果以顾客实际操作为准。说明：差评协商修改并非100%能成功，目前总体成功率60%左右，感谢理解！'
    )
    cursor.execute("SELECT phone FROM `t_phone` where shop_id=" + shopid + ";")
    results = cursor.fetchall()
    for row in results:
        # print(row[0])
        sendmsg(row[0], content)
    try:
        cursor.execute(
            "UPDATE t_ea_evaluate_revise_detial set reviser='admin' where shop_id ="
            + shopid
            + " and phones like '%"
            + phone
            + "%' and order_id ="
            + orderid
            + ";"
        )
        dbconn.commit()
    except:
        print("Process fail. Rollback.")
        dbconn.rollback()

    dbconn.close()
    cursor.close()
    return JsonResponse({'msg': 'ok'})


def sendmsg(to, content):
    appid = '24407'
    to = to
    content = content
    print(content)
    signature = 'ce61d45e3936c3645297213cde56f536'
    submaildata = (
        'appid='
        + appid
        + '&to='
        + to
        + '&content=【小评果】'
        + content
        + '退订回N &signature='
        + signature
    )
    submailurl = 'https://api.mysubmail.com/message/send.json'
    submailparam = submaildata.encode('utf8')
    subreq = urllib.request.Request(submailurl, data=submailparam)
    subres = urllib.request.urlopen(subreq)
    d2 = json.load(subres)
    print(d2)
