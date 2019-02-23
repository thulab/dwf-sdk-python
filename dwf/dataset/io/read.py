# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.15
#
# Title: methods for decoding and reading data
#
# Version 0.1
#

import numpy as np
import os
import tensorflow as tf
from PIL import Image
from urllib.parse import urlparse

from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms

from dwf.common.log import logger
from dwf.common.exception import *
from dwf.dataset.io.parser import *


def read_tfrecords_of_labeled_images(input_path, image_size, channel, num_classes):
    '''
        Read tfrecords of labeled images from given file, and resize images into specific
        size.

        Args:
            input_path - The given tfrecord file of labeled images, either HDFS address(hdfs://namenode:8020/test.tfrecords) or LOCAL addresss.
            image_size - The expected size of images.
        Return:
            labeled_images - The Dataset instance of labeled images.
        Raises:
            AssertionError - if input_path not exist

    '''
    # Whether an HDFS address
    if input_path.lower().startswith('hdfs://'):
        parsed_uri = urlparse(input_path)
        hdfs_service_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        hdfs_file_path = '{uri.path}'.format(uri=parsed_uri)
    else:
        if not os.path.isfile(input_path):
            logger.error('No file %s found.' % input_path)
            raise FILE_NOT_EXIST

    image_dataset = tf.data.TFRecordDataset(input_path)
    labeld_images = image_dataset.map(lambda x:labeled_image_parser(x, image_size, channel, num_classes))
    return labeld_images


def gen_tfrecords_of_boxed_images(images_input_path, bboxes_input_path, output_path, image_size):
    pass

def generate_pytorch_dataset(input_path, image_size, channel, num_classes):
    '''
        Read images from folder and return pytorch dataset.
        The folder must be as following:
            root/dog/xxx.png
            root/dog/xxy.png
            ...
        Args:
            input_path - The path of folder
            image_size - The expected size of images.
            channel - channel of images
            num_classed - class num
        Return:
            The Pytorch Dataset instance of labeled images.
        '''
    transform = transforms.Compose([transforms.Resize((image_size, image_size)), transforms.ToTensor(), transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))])
    pytorch_dataset = datasets.ImageFolder(input_path, transform = transform)
    return pytorch_dataset

def default_loader(path):
    '''
        Default image loader
        Args:
            path: path to one image
        Return:
            array(RGB)
    '''
    return Image.open(path).convert('RGB')

class TorchDatasetFromTxt(Dataset):
    def __init__(self, txt, transform=None, target_transform=None, loader=default_loader):
        fh = open(txt, 'r')
        imgs = []
        for line in fh:
            line = line.strip('\n')
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0],int(words[1])))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader
    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = self.loader(fn)
        if self.transform is not None:
            img = self.transform(img)
        return img,label
    def __len__(self):
        return len(self.imgs)

def generate_pytorch_dataset_from_txt(input_path, image_size, channel, num_class):
    '''
        Read images from txt file and return pytorch dataset.
        The txt file must be as following:
            image label
            eg. a.jpg 0
                b.jpg 1
                ...
        Args:
            input_path - The path of txt
            image_size - The expected size of images.
        Return:
            The Pytorch Dataset instance of labeled images.
    '''
    transform = transforms.Compose([transforms.Resize((image_size, image_size)), transforms.ToTensor(), transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))])
    pytorch_dataset_from_txt = TorchDatasetFromTxt(txt=input_path, transform = transform)
