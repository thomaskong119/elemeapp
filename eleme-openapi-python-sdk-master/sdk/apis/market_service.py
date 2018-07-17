# -*- coding: utf-8 -*-


# 服务市场服务
class MarketService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def sync_market_messages(self, start, end, offset, limit):
        """
        同步某一段时间内的服务市场消息
        :param start:开始时间
        :param end:结束时间
        :param offset:消息偏移量
        :param limit:查询消息数
        """
        return self.__client.call("eleme.market.syncMarketMessages", {"start": start, "end": end, "offset": offset, "limit": limit})

