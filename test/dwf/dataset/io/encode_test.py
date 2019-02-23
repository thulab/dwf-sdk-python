# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.15
#
# Title: Tests for encoding
#
# Version 0.1
#

import unittest
import os
from hdfs import *
from dwf.dataset.io.encode import *
from dwf.dataset.io.read import *
from dwf.common.config import test_config


class TestEncode(unittest.TestCase):

    def setUp(self):
        self.TEST_LOCAL_ADDRESS_PREFIX = test_config.get('LOCAL', 'TEST_LOCAL_ADDRESS_PREFIX')

    def test_encode_and_read_of_labeled_images(self):
        test_labeled_images_file_path = 'dwf/test/resources/labeled_images.txt'
        test_target_file_path = os.path.join(self.TEST_LOCAL_ADDRESS_PREFIX, 'labeled_images.tfrecords')
        gen_tfrecords_of_labeled_images(input_path=test_labeled_images_file_path, output_path=test_target_file_path, image_size=224)
        assert os.path.isfile(test_target_file_path)

        num_classes = 10
        labeled_images_dataset = read_tfrecords_of_labeled_images(test_target_file_path, 224, 3, num_classes)
        iterator = labeled_images_dataset.make_one_shot_iterator()
        img, label = iterator.get_next()
        assert img.shape == (224, 224, 3)
        assert label.shape == (num_classes)


    def test_encode_and_read_of_videos_from_clips_npz(self):
        test_npz_videos_file_path = 'dwf/test/resources/moving-mnist-train.npz'
        test_target_file_path = os.path.join(self.TEST_LOCAL_ADDRESS_PREFIX, 'moving-mnist-videos.tfrecords')
        video_shape = gen_tfrecords_of_videos_from_clips_npz(input_path=test_npz_videos_file_path, output_path=test_target_file_path)
        assert video_shape == (20, 64, 64, 1)

        videos_dataset = read_tfrecords_of_clips_videos(test_target_file_path, (20, 64, 64, 1))
        iterator = videos_dataset.make_one_shot_iterator()
        video = iterator.get_next()
        assert video.shape == (20, 64, 64, 1)


if __name__ == '__main__':
    unittest.main()

