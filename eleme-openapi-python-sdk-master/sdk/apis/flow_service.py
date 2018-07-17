# -*- coding: utf-8 -*-


# 餐厅入口流量服务
class FlowService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_entry_flow_stats_data(self, request):
        """
        根据时间段获取餐厅流量入口数据
        :param request:餐厅入口流量查询条件
        """
        return self.__client.call("eleme.flow.getEntryFlowStatsData", {"request": request})

