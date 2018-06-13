from sdk.oauth.oauth_client import OAuthClient
from sdk.apis.order_service import OrderService
from sdk.config import Config
from sdk.protocol.rpc_client import RpcClient
from sdk.apis.market_service import MarketService
from sdk.apis.shop_service import ShopService
import json
from datetime import datetime
from datetime import timedelta

shopid = 162965803
# token = {
#  "access_token" : "6dd11ae4ad6443f02bf913e68f650653"
# }
token = {
 "access_token" : ""
}
key = "7krZAkvpzm"
secret = "35ca3c7add3c05619f01e0dc6c63a4dd5f63fc46"
call_back_url = "https://sthgeleme.hz.taeapp.com/sthg/v1.3/authorize.jsp?appId=79237657"

config = Config(False, key, secret, call_back_url)
# 自己的日志处理方式,必须有info 和error 方法
class MyLog:
    def info(self, log):
        # print (u"my info log:{}".format(log))
        pass

    def error(self, log):
        print (u"my error log:{}".format(log))

config.set_log(MyLog())
token = json.dumps(token)

client = RpcClient(config, token)
# response = OrderService(client).get_all_orders(shop_id = 162965803, page_no = 1, page_size = 20, date = "2018-06-08")
ts = datetime.now()
te = ts + timedelta(days=1)
response = MarketService(client).sync_market_messages(ts.timestamp(), te.timestamp(), 0, 10)
response = response['list']
for index in range(len(response)):
    print(str(response[index]['userId'])+str(response[index]['phoneList']))
# shop_service = ShopService(client)
# shop = shop_service.get_shop(shopid)