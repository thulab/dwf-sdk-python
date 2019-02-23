# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.14
#
# Title: methods for encoding data
#
# Version 0.1
#

import numpy as np
import os
import tensorflow as tf
from PIL import Image
from dwf.common.log import logger 
from dwf.common.exception import *


def gen_tfrecords_of_labeled_images(input_path, output_path, image_size):
    '''
        Generate a file of tfrecords to store images represented by a given text file, which
        list the local address of images on the first column and the label number on the se-
        cond column.

        Args:
            input_path - The given file stored information of images.
            output_path - The output address of tfrecord file.
            image_size - The size of encoded images
        Raises:
            AssertionError - if input_path not exist

    '''
    # check path
    if not os.path.isfile(input_path):
        logger.error("File %s not exist." % input_path)
        raise FILE_NOT_EXIST

    # create target path
    parent_dir = os.path.dirname(output_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    writer = tf.python_io.TFRecordWriter(output_path)
    input_file = open(input_path)
    lines = input_file.readlines()
    input_file.close()
    with tf.Session() as sess:
        for i,line in enumerate(lines):
            img_path, img_label = line.split()
            img = Image.open(img_path)
            img = img.resize((image_size, image_size))
            img_raw = img.tobytes()
            label = int(img_label)
            features = {
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
            }
            example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(example.SerializeToString())
    writer.close()


def gen_tfrecords_of_videos_from_clips_npz(input_path, output_path):
    '''
        Generate a file of tfrecords to store videos represented by a given npz file, which
        store three dimensions, namely 'clips', 'dims', 'input_raw_data'. It is assumed that
        each video has the same length, which would be inferred by the shape of input_raw_d-
        ata. Another assumption is that the dimentsions of 'input_raw_data' is [num_vides,
        channel, weight, height].

        Args:
            input_path - The given file stored information of images.
            output_path - The output address of tfrecord file.

        Raises:
            FILE_NOT_EXIST - if input_path not exist.
            FILE_FORMAT_ERROR - if format of given file does not comfort to assumption.

        Returns:
            The shape of each videos

    '''
    # check path
    if not os.path.isfile(input_path):
        logger.error("File %s not exist." % input_path)
        raise FILE_NOT_EXIST

    # create target path
    parent_dir = os.path.dirname(output_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    writer = tf.python_io.TFRecordWriter(output_path)
    npz_data = np.load(input_path)
    # TODO The shape of clips is assumed to be [2, num_videos, 2],
    # Consider scalability when there is a need.
    clips_seperated = np.concatenate(npz_data['clips'], axis=1)
    # make dimensions comportable with TensorFlow with [num_videos, weight, height, channel]
    raw_tensor = np.transpose(npz_data['input_raw_data'],[0,2,3,1])
    screen_shape = np.shape(raw_tensor)[1:]
    num_videos = np.shape(clips_seperated)[0]
    if np.shape(clips_seperated) != (num_videos, 4):
        logger.error('The given npz file does not fit the assumed format.')
        raise FILE_FORMAT_ERROR
    with tf.Session() as sess:
        for i,clip_seperated in enumerate(clips_seperated):
            video = np.concatenate([raw_tensor[clip_seperated[0]:clip_seperated[1]], raw_tensor[clip_seperated[2]:clip_seperated[3]]])
            video_raw = video.tobytes()
            features = {
                'video': tf.train.Feature(bytes_list=tf.train.BytesList(value=[video_raw])),
            }
            example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(example.SerializeToString())
    writer.close()
    video_shape = list(screen_shape)
    video_shape.insert(0, 2 * (clips_seperated[0][1] - clips_seperated[0][0]))
    video_shape = tuple(video_shape)
    return video_shape



def gen_tfrecords_of_boxed_images(images_input_path, bboxes_input_path, output_path, image_size):
    pass

