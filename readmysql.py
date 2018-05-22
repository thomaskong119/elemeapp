import pymysql
  
dbconn=pymysql.connect(
  host="sthgelememassageread.mysql.rds.aliyuncs.com",
  database="ele_message",
  user="sthgadmin",
  password="Sthg123456",
  port=3306,
  charset='utf8'
 )

cursor = dbconn.cursor()

sqlcmd="SELECT * FROM t_ea_evaluate_revise_detial where phones like '%6101%';"

try:
   cursor.execute(sqlcmd)
   results = cursor.fetchall()
   print (results)
except:
   print ("Error: unable to fecth data")

dbconn.close()