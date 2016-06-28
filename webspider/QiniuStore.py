# -*- coding: utf-8 -*-
import requests
from conf.config import qiniu_config as qnconf
from qiniu import Auth, BucketManager, put_data
import logging
import hashlib

QINIU_ACCESS_KEY = qnconf["access_key"]
QINIU_SECRET_KEY = qnconf["secret_key"]
QINIU_DEFAULT_BUCKET = qnconf["bucket_name"]
QINIU_DEFAULT_URL_PREFIX = qnconf["domain"]


class QiniuCloud(object):
    """
    七牛云，上传图片
    """

    def __init__(self, access_key=QINIU_ACCESS_KEY, secret_key=QINIU_SECRET_KEY):
        self.auth = Auth(access_key, secret_key)

    def upload_by_fetch(self, remote_file_path, key):
        """
        通过远程url上传文件，但是可能报错，请使用upload()方法
        :param remote_file_path:
        :param key:
        :return:
        """
        pass
        # bucket = BucketManager(self.auth)
        # ret, info = bucket.fetch(remote_file_path, QINIU_DEFAULT_BUCKET, key)
        # print('ret: %s' % ret)
        # print('info: %s' % info)

    def upload(self, file_data, key):
        """
        通过二进制流上传文件
        :param file_data:   二进制数据
        :param key:         key
        :return:
        """
        try:
            token = self.auth.upload_token(QINIU_DEFAULT_BUCKET)
            ret, info = put_data(token, key, file_data)
        except Exception as e:
            logging.error('upload error, key: {0}, exception: {1}'.format(key, e))

        if info.status_code == 200:
            logging.info('upload data to qiniu ok, key: {0}'.format(key))
            return True
        else:
            logging.error('upload data to qiniu error, key: {0}'.format(key))
            return False

    def upload_pics(self, pic_list):
        """
        上传图片列表，如果上传成功，则保存到mysql中
        :param pic_list:        图片列表
        :return:
        """
        logging.info('in upload_pic_list...')
        pic_key_list = []
        for pic_url in pic_list:
            pic_suffix = '.jpg'
            # key = key_prefix + str(info_id) + '/' + datetime.now().strftime('%Y%m%d%H%M%S%f') + pic_suffix
            key = "cd/" + hashlib.sha1(pic_url).hexdigest() + pic_suffix
            pic_data = requests.get(pic_url)
            if self.upload(pic_data.content, key):
                pic_key_list.append((pic_url, QINIU_DEFAULT_URL_PREFIX + key))

        return pic_key_list
