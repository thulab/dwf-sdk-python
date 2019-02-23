# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.14
#
# Title: methods for uploading data to Specfic Datasource
#
# Version 0.1
#

from hdfs import *
import os


def upload_file_to_hdfs(hdfs_service_url, local_file_path, target_path):
    '''
        Upload a file to specific path on given HDFS system.

        Args:
            hdfs_service_url - The service address of HDFS.
            local_file_path - The local file to be uploaded.
            target_path - The target path to store the give file.
        Raises:
            AssertionError - if local_file_path not exist

    '''
    client = Client(hdfs_service_url)
    # check path is OK
    assert os.path.isfile(local_file_path)
    # create target path
    client.makedirs(target_path)
    client.upload(target_path, local_file_path)


