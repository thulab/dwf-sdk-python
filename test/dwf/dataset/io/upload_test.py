# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.14
#
# Title: Tests for uploading
#
# Version 0.1
#

import unittest
import os
from hdfs import *
from dwf.dataset.io.upload import *
from dwf.common.config import test_config

class TestUpload(unittest.TestCase):

    def setUp(self):
        self.TEST_HDFS_ADDRESS_PREFIX = test_config.get('HDFS', 'TEST_HDFS_ADDRESS_PREFIX')
        self.TEST_LOCAL_ADDRESS_PREFIX = test_config.get('LOCAL', 'TEST_LOCAL_ADDRESS_PREFIX')
        self.TEST_HDFS_SERVICE = test_config.get('HDFS', 'TEST_HDFS_SERVICE')
        self.client = Client(self.TEST_HDFS_SERVICE)
        self.client.delete(self.TEST_HDFS_ADDRESS_PREFIX, recursive=True)

    def test_upload_file_to_hdfs(self):
        test_hdfs_file_path = os.path.join(self.TEST_HDFS_ADDRESS_PREFIX, 'test_uploading.txt')
        test_local_file_path = os.path.join(self.TEST_LOCAL_ADDRESS_PREFIX, 'test_uploading.txt')
        open(test_local_file_path, 'a').close()
        upload_file_to_hdfs(hdfs_service_url=self.TEST_HDFS_SERVICE, local_file_path=test_local_file_path, target_path=test_hdfs_file_path)
        self.client.status(os.path.join(test_hdfs_file_path, 'test_uploading.txt'))


if __name__ == '__main__':
    unittest.main()
