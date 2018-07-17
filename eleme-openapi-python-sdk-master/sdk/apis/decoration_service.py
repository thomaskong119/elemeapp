# -*- coding: utf-8 -*-


# 门店装修服务
class DecorationService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def create_window(self, window):
        """
        连锁店总店创建橱窗
        :param window:新增的橱窗信息和其关联连锁店子店I和子店商品
        """
        return self.__client.call("eleme.decoration.windows.createWindow", {"window": window})

    def update_window(self, window):
        """
        连锁店总店修改橱窗
        :param window:修改的橱窗信息和其关联连锁店子店ID和子店商品
        """
        return self.__client.call("eleme.decoration.windows.updateWindow", {"window": window})

    def delete_window(self, window):
        """
        连锁店总店删除橱窗
        :param window:删除橱窗信息
        """
        return self.__client.call("eleme.decoration.windows.deleteWindow", {"window": window})

    def order_window(self, window):
        """
        连锁店总店对多个橱窗进行排序
        :param window:橱窗排序信息
        """
        return self.__client.call("eleme.decoration.windows.orderWindow", {"window": window})

    def get_window_by_id(self, burst_window_id):
        """
        连锁店总店根据橱窗ID获取橱窗详情
        :param burstWindowId:橱窗ID
        """
        return self.__client.call("eleme.decoration.windows.getWindowById", {"burstWindowId": burst_window_id})

    def get_window_by_shop_id(self, operate_shop_id):
        """
        连锁店总店获取橱窗信息集合
        :param operateShopId:连锁店总店ID
        """
        return self.__client.call("eleme.decoration.windows.getWindowByShopId", {"operateShopId": operate_shop_id})

    def create_sign(self, sign):
        """
        连锁店总店创建招贴
        :param sign:招贴信息和其关联连锁店子店ID
        """
        return self.__client.call("eleme.decoration.sign.createSign", {"sign": sign})

    def update_sign(self, sign_id, sign):
        """
        连锁店总店修改招贴
        :param signId:招贴ID
        :param sign:招贴信息和其关联连锁店子店ID
        """
        return self.__client.call("eleme.decoration.sign.updateSign", {"signId": sign_id, "sign": sign})

    def invalid_sign(self, sign_id, operate_shop_id):
        """
        连锁店总店作废招贴
        :param signId:招贴ID
        :param operateShopId:连锁店总店ID
        """
        return self.__client.call("eleme.decoration.sign.invalidSign", {"signId": sign_id, "operateShopId": operate_shop_id})

    def get_sign_history_image(self, sign):
        """
        连锁店总店获取历史上传过的招贴图片
        :param sign:查询条件
        """
        return self.__client.call("eleme.decoration.sign.getSignHistoryImage", {"sign": sign})

    def query_sign(self, sign):
        """
        连锁店总店分页查询店铺招贴
        :param sign:查询条件
        """
        return self.__client.call("eleme.decoration.sign.querySign", {"sign": sign})

    def get_sign_by_id(self, sign_id):
        """
        连锁店总店根据招贴ID查询店铺招贴详情
        :param signId:招贴ID
        """
        return self.__client.call("eleme.decoration.sign.getSignById", {"signId": sign_id})

    def create_poster(self, poster):
        """
        连锁店总店创建海报接口
        :param poster:海报信息和其关联连锁店子店I和子店商品
        """
        return self.__client.call("eleme.decoration.poster.createPoster", {"poster": poster})

    def update_poster(self, poster_id, poster):
        """
        连锁店总店修改海报
        :param posterId:海报ID
        :param poster:海报信息和其关联连锁店子店ID和子店商品
        """
        return self.__client.call("eleme.decoration.poster.updatePoster", {"posterId": poster_id, "poster": poster})

    def invalid_poster(self, poster):
        """
        连锁店总店作废海报
        :param poster:作废海报信息
        """
        return self.__client.call("eleme.decoration.poster.invalidPoster", {"poster": poster})

    def get_poster_detail_by_id(self, poster_id, operate_shop_id):
        """
        连锁店总店根据海报ID获取海报详情
        :param posterId:海报ID
        :param operateShopId:连锁店总店ID
        """
        return self.__client.call("eleme.decoration.poster.getPosterDetailById", {"posterId": poster_id, "operateShopId": operate_shop_id})

    def query_poster(self, poster):
        """
        连锁店总店根据条件查询海报信息集合
        :param poster:查询海报条件参数
        """
        return self.__client.call("eleme.decoration.poster.queryPoster", {"poster": poster})

    def get_poster_history_image(self, operate_shop_id):
        """
        连锁店总店获取历史上传过的海报图片
        :param operateShopId:连锁店总店ID
        """
        return self.__client.call("eleme.decoration.poster.getPosterHistoryImage", {"operateShopId": operate_shop_id})

    def create_brand_story(self, story):
        """
        连锁店总店新增品牌故事
        :param story:品牌故事信息和其关联连锁店子店ID
        """
        return self.__client.call("eleme.decoration.story.createBrandStory", {"story": story})

    def update_brand_story(self, brand_story_id, story):
        """
        连锁店总店更新品牌故事
        :param brandStoryId:品牌故事ID
        :param story:品牌故事信息和其关联连锁店子店ID
        """
        return self.__client.call("eleme.decoration.story.updateBrandStory", {"brandStoryId": brand_story_id, "story": story})

    def delete_brand_story(self, brand_story_id, operate_shop_id):
        """
        连锁店总店删除品牌故事
        :param brandStoryId:品牌故事ID
        :param operateShopId:连锁店总店店铺ID
        """
        return self.__client.call("eleme.decoration.story.deleteBrandStory", {"brandStoryId": brand_story_id, "operateShopId": operate_shop_id})

    def get_brand_story_by_id(self, brand_story_id):
        """
        连锁店总店查询当前设置的品牌故事信息
        :param brandStoryId:品牌故事ID
        """
        return self.__client.call("eleme.decoration.story.getBrandStoryById", {"brandStoryId": brand_story_id})

    def upload(self, image):
        """
        上传图片
        :param image:文件内容base64编码值
        """
        return self.__client.call("eleme.decoration.image.upload", {"image": image})

    def get_image(self, hash):
        """
        根据图片HASH值获取图片信息
        :param hash:图片HASH值
        """
        return self.__client.call("eleme.decoration.image.getImage", {"hash": hash})

