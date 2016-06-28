# -*- coding: utf-8 -*-
from qiniu import Auth
from qiniu import BucketManager, put_data
from twisted.internet import threads

from conf.config import qiniu_config as qnconf


class Qiniu(object):
    def __init__(self, uri):
        assert uri.startswith('http://')
        self.qn = Auth(qnconf['access_key'], qnconf['secret_key'])
        self.token = self.qn.upload_token(qnconf['bucket_name'])
        self.bucket = BucketManager(self.qn)

    # def stat_image(self, key):
    #     status, image_info = self.bucket.stat(qnconf['bucket_name'], key)
    #     last_modified = int(status['putTime'] / 1000000)
    #     return {'checksum': status['hash'], 'last_modified': last_modified}

    # def persist_image(self, key, image, buf, info):
    #     buf.seek(0)
    #     return threads.deferToThread(put_data, self.token, key, buf.getvalue())

    def get_file_stat(self, key):
        stat, error = self.bucket.stat(qnconf['bucket_name'], key)
        return stat

    def stat_file(self, path, info):
        def _onsuccess(stat):
            if stat:
                checksum = stat['hash']
                timestamp = stat['putTime'] / 10000000
                return {'checksum': checksum, 'last_modified': timestamp}
            else:
                return {}
        return threads.deferToThread(self.get_file_stat, path).addCallback(_onsuccess)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        buf.seek(0)
        return threads.deferToThread(put_data, self.token, path, buf.getvalue())
