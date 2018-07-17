from sdk.oauth.oauth_client import OAuthClient
from sdk.apis.order_service import OrderService
from sdk.config import Config
from sdk.protocol.rpc_client import RpcClient
from sdk.apis.market_service import MarketService
from sdk.apis.shop_service import ShopService
from sdk.apis.message_service import MessageService
import json
from datetime import datetime
from datetime import timedelta
import time

token = {
 "access_token" : ''
}
key = "7krZAkvpzm"
secret = "35ca3c7add3c05619f01e0dc6c63a4dd5f63fc46"
call_back_url = "https://sthgeleme.hz.taeapp.com/sthg/v1.3/authorize.jsp?appId=79237657"

# key = "UBQt2jl6qH"
# secret = "0757f08a215a3688d8ee80f04b99aa8c843b241a"
# call_back_url = "https://sthgele.hz.taeapp.com/authorize.jsp?appId=51767154"

config = Config(False, key, secret, call_back_url)
class MyLog:
    def info(self, log):
        # print (u"my info log:{}".format(log))
        pass

    def error(self, log):
        print (u"my error log:{}".format(log))

config.set_log(MyLog())
token = json.dumps(token)
client = RpcClient(config, token)

# response = MessageService(client).get_non_reached_messages(app_id = 79237657)
# print(response)

te = time.mktime(time.strptime(datetime.today().strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
ts = time.mktime(time.strptime((datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))

sumprice = 0
offset = 0
limit = 100

while True:
    response = MarketService(client).sync_market_messages(int(ts*1000), int(te*1000), offset, limit)
    for index in range(len(response['messages'])):
        sumprice += json.loads(response['messages'][index])['totalPrice']
    offset += limit
    if offset > response['count']:
        break

print(sumprice)