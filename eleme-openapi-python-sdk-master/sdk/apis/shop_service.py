# -*- coding: utf-8 -*-


# 店铺服务
class ShopService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_shop(self, shop_id):
        """
        查询店铺信息
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.shop.getShop", {"shopId": shop_id})

    def update_shop(self, shop_id, properties):
        """
        更新店铺基本信息
        :param shopId:店铺Id
        :param properties:店铺属性
        """
        return self.__client.call("eleme.shop.updateShop", {"shopId": shop_id, "properties": properties})

    def mget_shop_status(self, shop_ids):
        """
        批量获取店铺简要
        :param shopIds:店铺Id的列表
        """
        return self.__client.call("eleme.shop.mgetShopStatus", {"shopIds": shop_ids})

    def set_delivery_time(self, shop_id, delivery_basic_mins, delivery_adjust_mins):
        """
        设置送达时间
        :param shopId:店铺Id
        :param deliveryBasicMins:配送基准时间(单位分钟)
        :param deliveryAdjustMins:配送调整时间(单位分钟)
        """
        return self.__client.call("eleme.shop.setDeliveryTime", {"shopId": shop_id, "deliveryBasicMins": delivery_basic_mins, "deliveryAdjustMins": delivery_adjust_mins})

    def set_online_refund(self, shop_id, enable):
        """
        设置是否支持在线退单
        :param shopId:店铺Id
        :param enable:是否支持
        """
        return self.__client.call("eleme.shop.setOnlineRefund", {"shopId": shop_id, "enable": enable})

    def set_booking_status(self, shop_id, enabled, max_booking_days):
        """
        设置是否支持预定单及预定天数
        :param shopId:店铺id
        :param enabled:是否支持预订
        :param maxBookingDays:最大预定天数
        """
        return self.__client.call("eleme.shop.setBookingStatus", {"shopId": shop_id, "enabled": enabled, "maxBookingDays": max_booking_days})

    def get_oid_by_shop_ids(self, shop_ids):
        """
        批量通过店铺Id获取Oid
        :param shopIds:店铺Id的列表
        """
        return self.__client.call("eleme.shop.getOidByShopIds", {"shopIds": shop_ids})

    def update_busy_level_setting(self, shop_id, week_setting, date_setting):
        """
        更新店铺营业时间预设置
        :param shopId:店铺 id 
        :param weekSetting:一周营业时间预设置, 参考 OShopBusyLevelSetting weekSetting 字段定义 
        :param dateSetting:特定日期营业时间预设置, 参考 OShopBusyLevelSetting dateSetting 字段定义 
        """
        return self.__client.call("eleme.shop.updateBusyLevelSetting", {"shopId": shop_id, "weekSetting": week_setting, "dateSetting": date_setting})

    def get_busy_level_setting(self, shop_id):
        """
        获取店铺营业时间预设置
        :param shopId:店铺 id 
        """
        return self.__client.call("eleme.shop.getBusyLevelSetting", {"shopId": shop_id})

    def submit_open_store_message_audit(self, open_store_message):
        """
        提交开店申请接口
        :param openStoreMessage:开店申请表单
        """
        return self.__client.call("eleme.shop.setup.submitOpenStoreMessageAudit", {"openStoreMessage": open_store_message})

    def submit_open_store_for_mermaid(self, open_store_message):
        """
        星巴克提交开店申请接口
        :param openStoreMessage:开店申请表单
        """
        return self.__client.call("eleme.shop.setup.submitOpenStoreForMermaid", {"openStoreMessage": open_store_message})

    def update_open_store_message_audit(self, update_store_message_body):
        """
        更新申请信息接口
        :param updateStoreMessageBody:开店申请表单
        """
        return self.__client.call("eleme.shop.setup.updateOpenStoreMessageAudit", {"updateStoreMessageBody": update_store_message_body})

    def query_process_status_by_submit_id(self, submit_id):
        """
        查询请求状态接口
        :param submitId:请求提交id
        """
        return self.__client.call("eleme.shop.setup.queryProcessStatusBySubmitId", {"submitId": submit_id})

    def upload_image(self, image_base_6_4):
        """
        图片上传处理接口（5M以内图片）
        :param imageBase64:base64字节流
        """
        return self.__client.call("eleme.shop.setup.uploadImage", {"imageBase64": image_base_6_4})

    def upload_min_image(self, image_base_6_4):
        """
        图片上传处理接口（500K以内图片）
        :param imageBase64:base64字节流
        """
        return self.__client.call("eleme.shop.setup.uploadMinImage", {"imageBase64": image_base_6_4})

    def upload_image_with_remote_url(self, url):
        """
        远程上传图片接口
        :param url:图片url
        """
        return self.__client.call("eleme.shop.setup.uploadImageWithRemoteUrl", {"url": url})

