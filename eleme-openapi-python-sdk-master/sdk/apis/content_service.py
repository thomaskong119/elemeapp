# -*- coding: utf-8 -*-
import os
import time
import calendar
from ..efs_client import efsClient

# 视频服务
class ContentService:

    __client = None
    
    __video_max_size = 200 * 1024 * 1024

    __video_extend_list = ["MP4", "MOV"]

    def __init__(self, client):
        self.__client = client

    def upload_video(self, o_video_info, shop_id, video_type):
        """
        上传视频
        :param oVideoInfo:视频信息
        :param shopId:店铺Id
        :param videoType:视频类型
        """
        return self.__client.call("eleme.content.uploadVideo", {"oVideoInfo": o_video_info, "shopId": shop_id, "videoType": video_type})

    def get_efs_config(self, video_type):
        """
        获取efs配置
        :param videoType:视频类型
        """
        return self.__client.call("eleme.content.getEfsConfig", {"videoType": video_type})

    def set_video_bind_relation(self, video_id, biz_id, bind_biz_type):
        """
        建立视频与相对应的业务的关联关系
        :param videoId:视频Id
        :param bizId:业务Id
        :param bindBizType:业务类型
        """
        return self.__client.call("eleme.content.setVideoBindRelation", {"videoId": video_id, "bizId": biz_id, "bindBizType": bind_biz_type})

    def unset_video_bind_relation(self, video_id, biz_id, bind_biz_type):
        """
        取消视频与对应业务的关联关系
        :param videoId:视频Id
        :param bizId:业务Id
        :param bindBizType:业务类型
        """
        return self.__client.call("eleme.content.unsetVideoBindRelation", {"videoId": video_id, "bizId": biz_id, "bindBizType": bind_biz_type})

    def get_video_info(self, video_id):
        """
        通过视频id查询视频信息
        :param videoId:视频Id
        """
        return self.__client.call("eleme.content.getVideoInfo", {"videoId": video_id})

    def get_video_bind_info(self, video_id):
        """
        通过视频id获取所有相关联的业务关系
        :param videoId:视频Id
        """
        return self.__client.call("eleme.content.getVideoBindInfo", {"videoId": video_id})

    def upload_video_client(self, file_path, title, desc, video_type, shop_id):

        video_size = os.path.getsize(file_path)
        video_name = os.path.basename(file_path)
        video_extend = video_name[video_name.index(".") + 1:]

        if video_size > self.__video_max_size:
            raise BusinessException("视频大小不能超过200M")

        if video_extend.upper() not in self.__video_extend_list:
            raise BusinessException("只支持mp4和mov格式的视频")

        video_file = open(file_path)

        efs_config = self.get_efs_config(video_type)

        efs_client = efsClient(efs_config)

        client = efs_client.init()

        efs_key = str(shop_id) + '_' + str(calendar.timegm(time.gmtime()))

        version_id = efs_client.put_object(efs_key, efs_config['bucketName'], video_file)

        video_info = {
            "videoKey": efs_key,
            "versionId": str(version_id),
            "sizeInByte": video_size,
            "title": title,
            "description": desc
        }

        return self.upload_video(video_info, shop_id, video_type)
