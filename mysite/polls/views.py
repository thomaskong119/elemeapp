from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import json
import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

host="rm-2zeqp0878qi2f6xlnrw.mysql.rds.aliyuncs.com"
database="ele_message"
user="sthgadmin"
password="Sthg123456"
port=3306
charset='utf8'

sqlcmd="SELECT a.*,b.left_counter FROM t_ea_evaluate_revise_detial as a, t_ea_evaluate_revise as b where TO_DAYS(a.order_time) > TO_DAYS(NOW())-15 and a.shop_id = b.shop_id order by a.create_time desc;"

@csrf_exempt
def process(request):
    dbconn=pymysql.connect(host=host,database=database,user=user,password=password,port=port,charset=charset)
    cursor = dbconn.cursor()
    shopid = request.POST.get('shopid')
    phone = request.POST.get('phone')
    process = int(request.POST.get('process'))
    try:
        if process == 1:
            cursor.execute("UPDATE t_ea_evaluate_revise_detial set is_revise=1 where shop_id = " + shopid +" and phones like '%" + phone + "%';UPDATE t_ea_evaluate_revise SET left_counter = left_counter - 1 where shop_id= "+shopid +";")
            print ("Shopid=" + shopid + " Phone=" + phone + " Success.")
        elif process == 2:
            cursor.execute("UPDATE t_ea_evaluate_revise_detial set is_revise=2 where shop_id = " + shopid +" and phones like '%" + phone + "%';")
            print ("Shopid=" + shopid + " Phone=" + phone + " Fail.")
        elif process == 3:
            cursor.execute("UPDATE t_ea_evaluate_revise_detial set is_revise=1 where shop_id = " + shopid +" and phones like '%" + phone + "%';")
            print ("Shopid=" + shopid + " Phone=" + phone + " Passit.")
        dbconn.commit()
    except:
        print ("Process fail. Rollback.")
        dbconn.rollback()

    dbconn.close()
    cursor.close()
    return JsonResponse({'msg': 'ok'})

@csrf_exempt 
def index(request):
    dbconn=pymysql.connect(host=host,database=database,user=user,password=password,port=port,charset=charset)
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
        table.append({'shopid':row[1],'evaluateid':row[2],'beforerating':row[4],'beforecontent':row[5],'afterrating':row[6],'aftercontent':row[7],'createtime':row[8],'revisetime':row[9],'creator':row[10],'reviser':row[11],'isrevise':row12,'buyer':row[13],'phone':row[14],'beforetime':row[15],'aftertime':row[17],'ordertime':row[20],'appid':row[21],'orderid':row[22],'isrefund':row[23],'leftcount':row[24]})
    dbconn.close()
    cursor.close()
    return render(request, 'polls/index.html',{'results':table})
    