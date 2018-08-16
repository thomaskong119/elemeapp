# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from sdk.apis.market_service import MarketService
from sdk.apis.message_service import MessageService
from sdk.apis.order_service import OrderService
from sdk.apis.shop_service import ShopService
from sdk.apis.ugc_service import UgcService
from sdk.config import Config
from sdk.oauth.oauth_client import OAuthClient
from sdk.protocol.rpc_client import RpcClient

def _init(request):
    # token = {"access_token": '6fcb33768ed0961942e690bcc7dec81e'}
    token = {"access_token": ''}
    key = "7krZAkvpzm"
    secret = "35ca3c7add3c05619f01e0dc6c63a4dd5f63fc46"
    call_back_url = "https://sthgeleme.hz.taeapp.com/sthg/v1.3/authorize.jsp?appId=79237657"
    if request == '51767154':
        key = "UBQt2jl6qH"
        secret = "0757f08a215a3688d8ee80f04b99aa8c843b241a"
        call_back_url = "https://sthgele.hz.taeapp.com/authorize.jsp?appId=51767154"

    config = Config(False, key, secret, call_back_url)

    class MyLog:
        def info(self, log):
            # print (u"my info log:{}".format(log))
            pass

        def error(self, log):
            print(u"my error log:{}".format(log))

    config.set_log(MyLog())
    token = json.dumps(token)
    client = RpcClient(config, token)
    return client

# # data = {}
# # data['shopId'] = '159227530'
# # data['']
# data = {
#     "shopId": "150063478",
#     "startTime": "2018-07-11T00:00:00",
#     "endTime": "2018-07-17T00:00:00",
#     # "starRating": [
#     #   1,
#     #   2
#     # ],
#     "offset": 0,
#     "pageSize": 10,
#     "dataType": "ELEME",
# }

# response = UgcService(client).get_o_rate_result(data)
# print(response)

# response = MessageService(client).get_non_reached_messages(app_id = 79237657)
# print(response)

# te = time.mktime(time.strptime(datetime.today().strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
# ts = time.mktime(time.strptime((datetime.today()-timedelta(days=90)).strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
def getorder(request):

    client = _init(request)
    te = time.mktime(time.strptime((datetime.today()-timedelta(days=0)).strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    ts = time.mktime(time.strptime((datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d") + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))

    offset = 0
    limit = 300

    file_object = open('historyorder1.txt', 'w', encoding='utf-8')

    while True:
        response = MarketService(client).sync_market_messages(int(ts*1000), int(te*1000), offset, limit)
        for index in range(len(response['messages'])):
            # print(str(json.loads(response['messages'][index])))
            content = str(json.loads(response['messages'][index])) + '\n'
            file_object.write(content)
        offset += limit
        print(offset)
        if offset > response['count']:
            break

    file_object.close()

# getorder('51767154')
getorder('55498127')
# sumprice = 0
# offset = 0
# limit = 100

# while True:
#     response = MarketService(client).sync_market_messages(int(ts*1000), int(te*1000), offset, limit)
#     for index in range(len(response['messages'])):
#         sumprice += json.loads(response['messages'][index])['totalPrice']
#     offset += limit
#     if offset > response['count']:
#         break

# print(sumprice)
