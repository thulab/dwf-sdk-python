# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.16
#
# Title: parsers for different formats
#
# Version 0.1

import tensorflow as tf


def labeled_image_parser(image_record, image_size, num_channel, num_classes):
    '''
        Parse image from tfrecord file into image and label.

        Args:
            image_record - image information from tfrecord file.
            image_size - image size that specified when encoding.
            num_channel - number of channels that specified when encoding.
    '''
    features={
            'img_raw': tf.FixedLenFeature([], tf.string),
            'label': tf.FixedLenFeature([], tf.int64),
    }
    ori_features = tf.parse_single_example(
            image_record,
            features=features
    )
    image = tf.decode_raw(ori_features['img_raw'], tf.uint8)
    image = tf.reshape(image, [image_size, image_size, num_channel])
    image = tf.cast(image, tf.float32) / 255 - 0.5
    label = tf.cast(ori_features['label'], tf.uint8)
    label = tf.one_hot(label, depth=num_classes)
    label = tf.reshape(label, [num_classes])
    return image, label


def clips_video_parser(video_record, video_shape):
    '''
        Parse image from tfrecord file into videos.

        Args:
            video_record - videos from tfrecord file.
            video_shape - video size that specified when encoding.
    '''
    features={
            'video': tf.FixedLenFeature([], tf.string),
    }
    ori_features = tf.parse_single_example(
            video_record,
            features=features
    )
    video = tf.decode_raw(ori_features['video'], tf.uint8)
    video = tf.reshape(video, video_shape)
    return video


