# -*- coding: utf-8 -*-


# 活动服务
class ActivityService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_invited_activity_infos(self, shop_id):
        """
        查询店铺邀约活动信息(即将下线)
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.flash.getInvitedActivityInfos", {"shopId": shop_id})

    def apply_flash_activity(self, activity_id, activity_apply_info):
        """
        报名限量抢购活动(即将下线)
        :param activityId:活动Id
        :param activityApplyInfo:活动报名信息
        """
        return self.__client.call("eleme.activity.flash.applyFlashActivity", {"activityId": activity_id, "activityApplyInfo": activity_apply_info})

    def get_activity_apply_infos(self, activity_id, shop_id, page_no, page_size):
        """
        通过店铺Id和活动Id分页查询报名详情(即将下线)
        :param activityId:活动Id
        :param shopId:店铺Id
        :param pageNo:页码
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.flash.getActivityApplyInfos", {"activityId": activity_id, "shopId": shop_id, "pageNo": page_no, "pageSize": page_size})

    def update_activity_item_stock(self, activity_id, shop_id, item_id, stock):
        """
        修改活动菜品库存(即将下线)
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        :param stock:库存
        """
        return self.__client.call("eleme.activity.flash.updateActivityItemStock", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id, "stock": stock})

    def offline_flash_activity_item(self, activity_id, shop_id, item_id):
        """
        取消活动菜品(即将下线)
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        """
        return self.__client.call("eleme.activity.flash.offlineFlashActivityItem", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id})

    def invalid_shop_activity(self, activity_id, shop_id):
        """
        作废店铺与活动的关联关系(即将下线)
        :param activityId:活动Id
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.flash.invalidShopActivity", {"activityId": activity_id, "shopId": shop_id})

    def query_invited_food_activities(self, shop_id):
        """
        通过店铺Id查询该店铺被邀约的美食活动
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.food.queryInvitedFoodActivities", {"shopId": shop_id})

    def apply_food_activity(self, activity_id, activity_apply_info):
        """
        报名美食活动
        :param activityId:活动Id
        :param activityApplyInfo:活动报名信息
        """
        return self.__client.call("eleme.activity.food.applyFoodActivity", {"activityId": activity_id, "activityApplyInfo": activity_apply_info})

    def query_food_activities(self, activity_id, shop_id, page_no, page_size):
        """
        通过店铺Id和活动Id分页查询店铺已报名的美食活动
        :param activityId:活动Id
        :param shopId:店铺Id
        :param pageNo:页码
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.food.queryFoodActivities", {"activityId": activity_id, "shopId": shop_id, "pageNo": page_no, "pageSize": page_size})

    def update_food_activity_item_stock(self, activity_id, shop_id, item_id, stock):
        """
        修改美食活动的菜品库存
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        :param stock:库存
        """
        return self.__client.call("eleme.activity.food.updateFoodActivityItemStock", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id, "stock": stock})

    def offline_food_activity_item(self, activity_id, shop_id, item_id):
        """
        取消参与了美食活动的菜品
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        """
        return self.__client.call("eleme.activity.food.offlineFoodActivityItem", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id})

    def unbind_food_activity(self, activity_id, shop_id):
        """
        作废店铺与美食活动的关联关系
        :param activityId:活动Id
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.food.unbindFoodActivity", {"activityId": activity_id, "shopId": shop_id})

    def create_coupon_activity(self, create_info):
        """
        创建红包活动(即将下线)
        :param createInfo:创建红包活动的结构体
        """
        return self.__client.call("eleme.activity.coupon.createCouponActivity", {"createInfo": create_info})

    def give_out_coupons(self, shop_id, coupon_activity_id, mobiles):
        """
        向指定用户发放红包(即将下线)
        :param shopId:店铺Id
        :param couponActivityId:红包活动Id
        :param mobiles:需要发放红包的用户手机号列表
        """
        return self.__client.call("eleme.activity.coupon.giveOutCoupons", {"shopId": shop_id, "couponActivityId": coupon_activity_id, "mobiles": mobiles})

    def present_coupon(self, shop_id, mobile, coupon_template):
        """
        定向赠红包
        :param shopId:店铺Id
        :param mobile:需要发放红包的用户手机号
        :param couponTemplate:定向赠红包的模板信息
        """
        return self.__client.call("eleme.activity.coupon.presentCoupon", {"shopId": shop_id, "mobile": mobile, "couponTemplate": coupon_template})

    def query_coupon_activities(self, shop_id, coupon_activity_type, activity_status, page_no, page_size):
        """
        分页查询店铺红包活动信息(即将下线)
        :param shopId:店铺Id
        :param couponActivityType:红包活动类型
        :param activityStatus:活动状态
        :param pageNo:页码（第几页）
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.coupon.queryCouponActivities", {"shopId": shop_id, "couponActivityType": coupon_activity_type, "activityStatus": activity_status, "pageNo": page_no, "pageSize": page_size})

    def query_received_coupon_details(self, shop_id, coupon_activity_id, coupon_status, page_no, page_size):
        """
        分页查询店铺红包领取详情(即将下线)
        :param shopId:店铺Id
        :param couponActivityId:红包活动Id
        :param couponStatus:红包状态
        :param pageNo:页码（第几页）
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.coupon.queryReceivedCouponDetails", {"shopId": shop_id, "couponActivityId": coupon_activity_id, "couponStatus": coupon_status, "pageNo": page_no, "pageSize": page_size})

    def host_shops(self, shop_ids, hosted_type, discounts):
        """
        托管单店红包服务
        :param shopIds:餐厅id列表,长度不能超过20
        :param hostedType:红包服务业务类型,暂只支持超级会员,"SUPER_VIP"
        :param discounts:扣减额,请设置在[4,15]元,小数点后最多1位
        """
        return self.__client.call("eleme.activity.coupon.hostShops", {"shopIds": shop_ids, "hostedType": hosted_type, "discounts": discounts})

    def query_host_info(self, shop_ids, hosted_type):
        """
        查询红包服务托管情况
        :param shopIds:餐厅id列表,长度不能超过20
        :param hostedType:红包服务业务类型,暂只支持超级会员,"SUPER_VIP"
        """
        return self.__client.call("eleme.activity.coupon.queryHostInfo", {"shopIds": shop_ids, "hostedType": hosted_type})

    def unhost_shops(self, shop_ids, hosted_type):
        """
        取消托管单店红包服务
        :param shopIds:餐厅id列表,长度不能超过20
        :param hostedType:红包服务业务类型,暂只支持超级会员,"SUPER_VIP"
        """
        return self.__client.call("eleme.activity.coupon.unhostShops", {"shopIds": shop_ids, "hostedType": hosted_type})

    def rehost_shop(self, shop_id, hosted_type, o_activity_service_details):
        """
        更改单店红包服务托管方式
        :param shopId:店铺Id
        :param hostedType:红包服务业务类型,暂只支持超级会员,"SUPER_VIP"
        :param oActivityServiceDetails:服务内容
        """
        return self.__client.call("eleme.activity.coupon.rehostShop", {"shopId": shop_id, "hostedType": hosted_type, "oActivityServiceDetails": o_activity_service_details})

    def present_target_coupons(self, shop_id, target_list, target_list_type, target_coupon_detail):
        """
        定向赠红包(单店红包)
        :param shopId:店铺id
        :param targetList:目标列表
        :param targetListType:目标类型
        :param targetCouponDetail:定向赠红包模板细节
        """
        return self.__client.call("eleme.activity.coupon.presentTargetCoupons", {"shopId": shop_id, "targetList": target_list, "targetListType": target_list_type, "targetCouponDetail": target_coupon_detail})

    def present_common_target_coupons(self, chain_id, target_list, target_list_type, common_target_coupon_detail):
        """
        定向赠通用红包
        :param chainId:连锁店id
        :param targetList:目标列表
        :param targetListType:目标类型
        :param commonTargetCouponDetail:通用定向赠红包模板细节
        """
        return self.__client.call("eleme.activity.coupon.presentCommonTargetCoupons", {"chainId": chain_id, "targetList": target_list, "targetListType": target_list_type, "commonTargetCouponDetail": common_target_coupon_detail})

    def query_target_coupon_info(self, target_coupon_query_request):
        """
        分页查询店铺的定向赠红包信息
        :param targetCouponQueryRequest:定向赠红包查询入参对象
        """
        return self.__client.call("eleme.activity.coupon.queryTargetCouponInfo", {"targetCouponQueryRequest": target_coupon_query_request})

