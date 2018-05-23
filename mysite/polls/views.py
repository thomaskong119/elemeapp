from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import json
  
dbconn=pymysql.connect(
  host="sthgelememassageread.mysql.rds.aliyuncs.com",
  database="ele_message",
  user="sthgadmin",
  password="Sthg123456",
  port=3306,
  charset='utf8'
 )

cursor = dbconn.cursor()

# sqlcmd="SELECT * FROM t_ea_evaluate_revise_detial where phones like '%6101%';"

sqlcmd="SELECT * FROM `t_ea_evaluate_revise_detial` where TO_DAYS(order_time) > TO_DAYS(NOW())-15 order by create_time desc;"

try:
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
        table.append({'shopid':row[1],'evaluateid':row[2],'beforerating':row[4],'beforecontent':row[5],'afterrating':row[6],'aftercontent':row[7],'createtime':row[8],'revisetime':row[9],'creator':row[10],'reviser':row[11],'isrevise':row12,'buyer':row[13],'phone':row[14],'beforetime':row[15],'aftertime':row[17],'ordertime':row[20],'appid':row[21],'orderid':row[22],'isrefund':row[23]})

#    for row in results: 
#        print (row)
#        shopid = row[1]
#        evaluateid = row[2]
#        beforerating = row[4]
#        beforecontent = row[5]
       
except:
   print ("Error: unable to fecth data")

dbconn.close()
cursor.close()

def index(request):
    return render(request, 'polls/index.html',{'results':table})