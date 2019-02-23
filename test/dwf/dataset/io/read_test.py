# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: jinying(sherryying003@gmail.com)
# Initial Date: 2018.07.19
#
# Title: Tests for uploading
#
# Version 0.1
#

import unittest
import os
from hdfs import *
from dwf.dataset.io import read
from dwf.common.config import test_config

class TestUpload(unittest.TestCase):

    def setUp(self):
        self.input_path = "/home/xlearn/dataset/imagenet_20"
        self.input_path_txt = "/home/xlearn/dataset/imagenet/imagenet_val_list_10.txt" 
        self.image_size = 64
        self.channel = 3
        self.num_classes = 20
        self.num_classes2 = 10

    def test_generate_pytorch_dataset(self):
        read.generate_pytorch_dataset(self.input_path,self.image_size, self.channel, self.num_classes)
    
    def test_generate_pytorch_dataset_from_txt(self):
        read.generate_pytorch_dataset_from_txt(self.input_path_txt, self.image_size, self.channel, self.num_classes2)

if __name__ == '__main__':
    unittest.main()
